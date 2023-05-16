# 평가 함수들을 제공하는 모듈

import matplotlib.pyplot as plt
from sklearn.metrics import (confusion_matrix, 
                             ConfusionMatrixDisplay, 
                             recall_score, 
                             accuracy_score, 
                             precision_score, 
                             f1_score)
import numpy as np
import seaborn as sns

def plot_confusion_matrix(y, pred, title=None):
    """
    confusion matrix를 시각화하는 함수
    [parameter]
        y:ndarray - 정답(ground truth)
        pred: ndarray - 모델이 추정한 값
        title: str - 그래프의 제목(title)
    """
    cm = confusion_matrix(y, pred)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot(cmap='Blues')
    if title:
        plt.title(title)
    plt.show()
    
def print_metrics_classification(y, pred, title=None):  
    """
    분류 평갖치표 점수들을 출력하는 함수.
    accuracy, recall, precision, f1 score 를 출력
    [parameter]
        y:ndarray - 정답
        pred:ndarray - 모델 추정값
        title:str - 제목
    """
    if title:
        print(f"=========={title}==========")
    print(f"정확도(Accuracy): {accuracy_score(y, pred)}")
    print(f"재현율(Recall) : {recall_score(y, pred)}")
    print(f"정밀도(Precision): {precision_score(y, pred)}")
    print(f"F1 Score: {f1_score(y, pred)}")

def cm_viz(y_true, y_pred, cmap = 'Reds', color = 'r', figsize=(8, 8), title=None):
    """Confusion Matrix 시각화, 정확도, 정밀도, 재현율, F1-score를 한번에 출력

    Args:
        y_true: 정답 데이터
        y_pred: 예측 데이터
        cmap: heatmap 색상
        color: 바차트 색상
        figsize: 그래프 크기
        title: 그래프 제목
    """
    
    fig = plt.figure(figsize=figsize)
    if title is not None:
        fig.suptitle(title, fontsize=16)
    axs = fig.subplots(2, 2)
    cm_ax, recall_ax = axs[0]
    acc_prec_ax, f1_ax = axs[1]
    # 혼동행렬 생성
    cm = confusion_matrix(y_true, y_pred)
    tags= ['TN', 'FP', 'FN', 'TP']
    counts = [f'{value:0.0f}' for value in cm.flatten()]
    labels = [f'{t}\n{c}' for t, c in zip(tags, counts)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(cm,
                annot=labels,
                cmap=cmap,
                fmt='',
                xticklabels=['Negative', 'Positive'],
                yticklabels=['Negative', 'Positive'],
                ax=cm_ax,
                )
    cm_ax.set_xlabel('Predicted Label')
    cm_ax.set_ylabel('True Label')
    cm_ax.set_title('Confusion Matrix')
    
    
    
    # precision, accuracy ax에 바차트로 표시
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    acc_prec_ax.bar(['Accuracy', 'Precision'], [acc*100, prec*100], color=color)
    acc_prec_ax.set_ylim(0, 100)
    acc_prec_ax.set_title('Accuracy & Precision')
    acc_prec_ax.set_ylabel('Score')
    # precision accuracy 퍼센트로 표시
    acc_prec_ax.text(0, acc*100, f'{acc*100:.2f}%', ha='center', va='bottom')
    acc_prec_ax.text(1, prec*100, f'{prec*100:.2f}%', ha='center', va='bottom')
    
    # recall ax에 가로 바차트로 spec, recall 표시-> 'Recall', 'Specificity' 표시는 세로로
    rc = recall_score(y_true, y_pred)
    spec = cm[0, 0] / (cm[0, 0] + cm[0, 1])
    recall_ax.barh(['Recall', 'Specificity'], [rc*100, spec*100], color=color)
    recall_ax.set_xlim(0, 100)
    recall_ax.set_title('Specificity & Recall')
    # recall 퍼센트로 표시
    recall_ax.text(rc*100, 0, f'{rc*100:.2f}%', ha='left', va='center')
    recall_ax.text(spec*100, 1, f'{spec*100:.2f}%', ha='left', va='center')
    
    # f1 ax에 바차트로 표시
    f1 = f1_score(y_true, y_pred)
    f1_ax.bar(['F1'], [f1 * 100], color=color, width=0.1, align='center')
    f1_ax.set_ylim(0, 100)
    f1_ax.set_title('F1')
    f1_ax.set_ylabel('Score')
    # f1 퍼센트로 표시
    f1_ax.text(0, f1*100, f'{f1*100:.2f}%', ha='center', va='bottom')
    
    plt.show()


#================================================================
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier

# from metrics import plot_confusion_matrix as pcm, print_metrics_classification as pmc

# # 1.모델생성
# tree = DecisionTreeClassifier(max_depth=3, random_state=0)
# rfc = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=0)

# # 2. 모델 학습
# tree.fit(X_train,y_train)
# rfc.fit(X_train, y_train)

# # 3. 평가
# ## 추론
# pred_train_tree = tree.predict(X_train)
# pred_test_tree = tree.predict(X_test)

# pred_train_rfc = rfc.predict(X_train)
# pred_test_rfc = rfc.predict(X_test)

# # confusion matrix
# pcm(y_train, pred_train_tree, "DT train set")
# pcm(y_test, pred_test_tree, "DT test set")
# pcm(y_train, pred_train_rfc, 'RFC train set')
# pcm(y_test, pred_test_rfc, 'RFC test set')
