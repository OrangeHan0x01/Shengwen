# -*- coding: utf-8 -*-
import numpy as np
import audio_process.voice_activity_detect as vad
import audio_process.vq_lbg as vqlbg
import librosa
import os
import shutil
from sklearn.cluster import KMeans
from collections import OrderedDict
import soundfile as sf

def cluster_greedy(feature_vectors, cluster_list):
    current_cluster_number = len(cluster_list)
    for index, key in enumerate(feature_vectors.keys()):
        if index == 0:
            base_feature = feature_vectors[key]
            cluster_list[str(current_cluster_number)]=list()
            temp = cluster_list[str(current_cluster_number)]
            temp.append(key)
            cluster_list[str(current_cluster_number)] = temp
        else:
            bic_dis = cluter_on_bic(base_feature, feature_vectors[key])
            if bic_dis < 50:
                temp = cluster_list[str(current_cluster_number)]
                temp.append(key)
                cluster_list[str(current_cluster_number)] = temp
    for i in cluster_list[str(current_cluster_number)]:
        feature_vectors.pop(i)
def cluter_on_bic(mfcc_s1, mfcc_s2):
    mfcc_s = np.concatenate((mfcc_s1, mfcc_s2), axis=1)
    m, n = mfcc_s.shape
    m, n1 = mfcc_s1.shape
    m, n2 = mfcc_s2.shape
    sigma0 = np.cov(mfcc_s).diagonal()
    eps = np.spacing(1)
    realmin = np.finfo(np.double).tiny
    det0 = max(np.prod(np.maximum(sigma0,eps)),realmin)
    part1 = mfcc_s1
    part2 = mfcc_s2
    sigma1 = np.cov(part1).diagonal()
    sigma2 = np.cov(part2).diagonal()
    det1 = max(np.prod(np.maximum(sigma1, eps)), realmin)
    det2 = max(np.prod(np.maximum(sigma2, eps)), realmin)
    BIC = 0.5 * (n * np.log(det0) - n1 * np.log(det1) - n2 * np.log(det2)) - 0.5 * (m + 0.5 * m * (m + 1)) * np.log(n)
    return BIC

def compute_bic(mfcc_v,delta):
    m, n = mfcc_v.shape
    sigma0 = np.cov(mfcc_v).diagonal()
    eps = np.spacing(1)
    realmin = np.finfo(np.double).tiny
    det0 = max(np.prod(np.maximum(sigma0,eps)),realmin)
    flat_start = 5
    range_loop = range(flat_start,n,delta)
    x = np.zeros(len(range_loop))
    iter = 0
    for index in range_loop:
        part1 = mfcc_v[:, 0:index]
        part2 = mfcc_v[:, index:n]
        sigma1 = np.cov(part1).diagonal()
        sigma2 = np.cov(part2).diagonal()
        det1 = max(np.prod(np.maximum(sigma1, eps)), realmin)
        det2 = max(np.prod(np.maximum(sigma2, eps)), realmin)
        BIC = 0.5*(n*np.log(det0)-index*np.log(det1)-(n-index)*np.log(det2))-0.5*(m+0.5*m*(m+1))*np.log(n)
        x[iter] = BIC
        iter = iter + 1
    maxBIC = x.max()
    maxIndex = x.argmax()
    if maxBIC>0:
        return range_loop[maxIndex]-1
    else:
        return -1

def speech_segmentation(mfccs):
    wStart = 0
    wEnd = 200
    wGrow = 200
    delta = 25
    m, n = mfccs.shape
    store_cp = []
    index = 0
    while wEnd < n:
        featureSeg = mfccs[:, wStart:wEnd]
        detBIC = compute_bic(featureSeg, delta)
        index = index + 1
        if detBIC > 0:
            temp = wStart + detBIC
            store_cp.append(temp)
            wStart = wStart + detBIC + 200
            wEnd = wStart + wGrow
        else:
            wEnd = wEnd + wGrow
    return np.array(store_cp)

def multi_segmentation(file,sr,frame_size,frame_shift,save_dir = '',cluster_method = None,save_seg=1):
    y, sr = librosa.load(file, sr=sr)
    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=12, hop_length=frame_shift, n_fft=frame_size)
    seg_point = speech_segmentation(mfccs / mfccs.max())
    seg_point = seg_point * frame_shift
    seg_point = np.insert(seg_point, 0, 0)
    seg_point = np.append(seg_point, len(y))
    rangeLoop = range(len(seg_point) - 1)
    output_segpoint = []
    for i in rangeLoop:
        temp = y[seg_point[i]:seg_point[i + 1]]
        max_mean = np.mean(temp[temp.argsort()[-800:]])
        if max_mean < 0.005:
            continue
        x1, x2 = vad.vad(temp, sr=sr, framelen=frame_size, frameshift=frame_shift)
        if len(x1) == 0 or len(x2) == 0:
            continue
        elif seg_point[i + 1] == len(y):
            continue
        else:
            output_segpoint.append(seg_point[i + 1])
    if save_seg:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        else:
            shutil.rmtree(save_dir)
            os.makedirs(save_dir)
        save_segpoint = output_segpoint.copy()
        save_segpoint.insert(0,0)
        save_segpoint.append(len(y))
        for i in range(len(save_segpoint)-1):
            tempAudio = y[save_segpoint[i]:save_segpoint[i+1]]
            try:
                librosa.output.write_wav(save_dir+'/'+"%s.wav"%i,tempAudio,sr)
            except:
                sf.write(save_dir+'/'+"%s.wav"%i, tempAudio, sr, subtype='PCM_16')#原文件不是这种方法，但是librosa较新版本中删除了上一种方法，比赛项目打算采用较新的版本，故进行修改，使两种方法同时存在--OrangeHan0x01
    if cluster_method == 'kmeans':
        classify_segpoint = output_segpoint.copy()
        classify_segpoint.insert(0, 0)
        classify_segpoint.append(len(y))
        vq_features = np.zeros((len(classify_segpoint) - 1, 12), dtype=np.float32)
        for i in range(len(classify_segpoint) - 1):
            tempAudio = y[classify_segpoint[i]:classify_segpoint[i + 1]]
            mfccs = librosa.feature.mfcc(tempAudio, sr, n_mfcc=12, hop_length=frame_shift, n_fft=frame_size)
            mfccs = mfccs / mfccs.max()
            vq_code = np.mean(mfccs, axis=1)
            vq_features[i, :] = vq_code.reshape(1, vq_code.shape[0])
        K = range(1,len(classify_segpoint))
        square_error = []
        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=0).fit(vq_features)
            square_error.append(kmeans.inertia_)
        k_n = input("Please input the best K value: ")
        kmeans = KMeans(int(k_n), random_state=0).fit(vq_features)
        print("The lables for",len(kmeans.labels_),"speech segmentation belongs to the clusters below:")
        for i in range(len(kmeans.labels_)):
            print(kmeans.labels_[i],"")

    if cluster_method == "bic":
        classify_segpoint = output_segpoint.copy()
        classify_segpoint.insert(0, 0)
        classify_segpoint.append(len(y))
        feature_vectors = OrderedDict()
        for i in range(len(classify_segpoint) - 1):
            tempAudio = y[classify_segpoint[i]:classify_segpoint[i + 1]]
            mfccs = librosa.feature.mfcc(tempAudio, sr, n_mfcc=12, hop_length=frame_shift, n_fft=frame_size)
            mfccs = mfccs / mfccs.max()
            feature_vectors[str(i)] = mfccs
        cluster_list = {}
        while len(feature_vectors.keys())> 0 :
            cluster_greedy(feature_vectors, cluster_list)
        print('There are total %d clusters'%(len(cluster_list)), 'and they are listed below: ')
        for index, key in enumerate(cluster_list.keys()):
            print('cluster %d'%(index), ": ", cluster_list[key])
    return (np.asarray(output_segpoint) / float(sr))
