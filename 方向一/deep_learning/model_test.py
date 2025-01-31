from keras.utils import plot_model
import pickle
from keras.preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from keras.models import Model
from keras.layers import Dense, Embedding, Input, SpatialDropout1D
from keras.layers import Conv1D, Flatten, Dropout, MaxPool1D, GlobalAveragePooling1D, concatenate, GlobalMaxPooling1D
from keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from keras.utils import to_categorical
import time
import numpy as np
from keras import backend as K#keras后端
from sklearn.model_selection import StratifiedKFold
from keras.models import load_model
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import xgboost as xgb
from sklearn.feature_extraction.text import TfidfVectorizer

model_path="./model/"
cnn_model_path=model_path+"model_weight_train_cnn_"
cnn_and_lstm_model_path=model_path+"model_weight_text_cnn_and_lstm_"
lstm_model_path=model_path+"model_weight_lstm_"
tfidf_path=model_path+"tfidf_"

def plot_confusion_matrix(cm, title='Confusion Matrix'):
    labels=[0,1,2,3,4,5,6]
    plt.imshow(cm, interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def plot_matrix(name,y_test,y_pred):
    tick_marks = np.array(range(7)) + 0.5
    cm = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(12, 8), dpi=120)
    ind_array = np.arange(7)
    x, y = np.meshgrid(ind_array, ind_array)

    for x_val, y_val in zip(x.flatten(), y.flatten()):
        c = cm_normalized[y_val][x_val]
        if c > 0.01:
            plt.text(x_val, y_val, "%0.2f" % (c,), color='white', fontsize=7, va='center', ha='center')
    # offset the tick
    plt.gca().set_xticks(tick_marks, minor=True)
    plt.gca().set_yticks(tick_marks, minor=True)
    plt.gca().xaxis.set_ticks_position('none')
    plt.gca().yaxis.set_ticks_position('none')
    plt.grid(True, which='minor', linestyle='-')
    plt.gcf().subplots_adjust(bottom=0.15)

    plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')
    # show confusion matrix
    plt.savefig('./result/' + name +'_confusion_matrix.jpg', format='jpeg')
    # plt.show()

def deep_learn_model_test_tfidf(name,path,X_test):
    tpath = path
    meta_train = np.zeros(shape=(len(files), 2))
    ac = 0
    pe = 0
    re = 0
    f = 0
    for i in range(3,10):
        path = tpath + str(i) + ".model"
        print("model: " + path)
        tar = xgb.Booster(model_file=path)
        x_test = xgb.DMatrix(X_test)
        y_pred = tar.predict(x_test)
        meta_train[:] = y_pred
        # predict_type_list = []
        # for l in y_pred:
        #     l_tmp = l.tolist()
        #     predict_type = l_tmp.index(max(l_tmp))
        #     predict_type_list.append(predict_type)
        # # 准确率
        # accuracy = metrics.accuracy_score(y_test, predict_type_list)
        # print("准确率： " + str(accuracy))
        # ac += accuracy
        # # 精确率
        # precision = metrics.precision_score(y_test, predict_type_list, average='macro')
        # print("精确率： " + str(precision))
        # pe += precision
        # # 召回率
        # recall = metrics.recall_score(y_test, predict_type_list, average='macro')
        # print("召回率： " + str(recall))
        # re += recall
        # # F1-score
        # f1 = metrics.f1_score(y_test, predict_type_list, average='weighted')
        # print("F1-score： " + str(f1))
        # f+=f1

    #     # 混淆矩阵
    #     plot_matrix(name + "_" + str(i), y_test, predict_type_list)
    #
        with open(name+"_result_"+str(i)+"_train.pkl", 'wb') as f:
            pickle.dump(meta_train, f)
    # print("平均：")
    # print("准确率： " + str(ac / 5))
    # print("精确率： " + str(pe / 5))
    # print("召回率： " + str(re / 5))
    # print("F1-score： " + str(f / 5))


def deep_learn_model_test(name,path,X_test):
    meta_train = np.zeros(shape=(len(files), 2))
    tpath=path
    # ac=0
    # pe=0
    # re=0
    # f=0

    for i in range(4,10):
        path=tpath+str(i)+".h5"
        print("model: "+path)
        #加载模型
        model=load_model(path)
        y_pred=model.predict(X_test)
        meta_train[:] = y_pred
        # predict_type_list = []
        # for l in y_pred:
        #     l_tmp = l.tolist()
        #     predict_type = l_tmp.index(max(l_tmp))
        #     predict_type_list.append(predict_type)

        # cnt1 = 0
        # cnt2 = 0
        # for t in range(0, len(predict_type_list)):
        #     if predict_type_list[t] == y_test[t]:
        #         cnt1 += 1
        #     else:
        #         cnt2 += 1
        #
        # print("Train Accuary: %.2f%%" % (100.0 * cnt1 / (cnt1 + cnt2)))
        # # y_test = list(y_test)
        # print(np.shape(X_test))
        # print(np.shape(y_test))
        # # print(model.evaluate(X_test, y_test,show_accuracy=True, verbose=0))
        # # 准确率
        # accuracy = metrics.accuracy_score(y_test, predict_type_list)
        # print("准确率： " + str(accuracy))
        # ac+=accuracy
        # # 精确率
        # precision = metrics.precision_score(y_test, predict_type_list, average='macro')
        # print("精确率： " + str(precision))
        # pe+=precision
        # # 召回率
        # recall = metrics.recall_score(y_test, predict_type_list, average='macro')
        # print("召回率： " + str(recall))
        # re+=recall
        # # F1-score
        # f1 = metrics.f1_score(y_test, predict_type_list, average='weighted')
        # print("F1-score： " + str(f1))
        # f+=f1
    #     # #混淆矩阵
    #     plot_matrix(name+"_"+str(i), y_test, predict_type_list)
    #     # # 绘制模型图
    #     plot_model(model,to_file=name+"_model.png")
    #
        with open(name+"_result_"+str(i)+"_train.pkl", 'wb') as f:
            pickle.dump(meta_train, f)
    # print("平均：")
    # print("准确率： " + str(ac/5))
    # print("精确率： " + str(pe/5))
    # print("召回率： " + str(re/5))
    # print("F1-score： " + str(f/5))


if __name__ =='__main__':
    # 配置运行参数
    config = K.tf.ConfigProto()
    config.gpu_options.allow_growth = True
    session = K.tf.Session(config=config)


    with open("dynamic_feature_train.csv.pkl", "rb") as f:
        names = pickle.load(f)
        files = pickle.load(f)

    maxlen = 2000

    #tfidf
    vectorizer = pickle.load(open('tfidf_transformer.pkl', 'rb'))
    train_features = vectorizer.transform(files)

    #deep learning
    tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
    x_test_word_ids = tokenizer.texts_to_sequences(files)
    x_test_padded_seqs = pad_sequences(x_test_word_ids, maxlen=maxlen)

    # deep_learn_model_test("lstm",lstm_model_path,x_test_padded_seqs,labels_d)
    deep_learn_model_test("cnn",cnn_model_path, x_test_padded_seqs)
    # deep_learn_model_test("cnn_and_lstm",cnn_and_lstm_model_path, x_test_padded_seqs)
    # deep_learn_model_test_tfidf("tfidf",tfidf_path, train_features)
    K.clear_session()