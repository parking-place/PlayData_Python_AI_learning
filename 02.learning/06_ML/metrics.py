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
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, average_precision_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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
    
def print_metrics_classification(y, pred, title=None, pos_proba=None):  
    """
    분류 평가지표 점수들을 출력하는 함수.
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
    if pos_proba is not None:
        print(f'Averaged Precision: {average_precision_score(y, pos_proba)}')
        print(f"ROC-AUC Score: {roc_auc_score(y, pos_proba)}")
        
def print_metrics_regression(y, pred, title=None):
    """
    회귀 평가지표 점수들을 출력하는 함수.
    MAE, MSE, RMSE, R2 를 출력
    [parameter]
        y:ndarray - 정답
        pred:ndarray - 모델 추정값
        title:str - 제목
    """
    if title:
        print(f"=========={title}==========")
    print(f"MAE: {mean_absolute_error(y, pred)}")
    print(f"MSE: {mean_squared_error(y, pred)}")
    print(f"RMSE: {mean_squared_error(y, pred, squared=False)}")
    print(f"R2 Score: {r2_score(y, pred)}")

# PR Curve 시각화 함수
def plot_pr_curve(y, pos_proba, title=None, figsize=(6, 6)):
    from sklearn.metrics import precision_recall_curve, average_precision_score, PrecisionRecallDisplay
    precisions, recalls, thresholds = precision_recall_curve(y, pos_proba)
    ap = average_precision_score(y, pos_proba)
    disp = PrecisionRecallDisplay(precision=precisions, recall=recalls, average_precision=ap, estimator_name=title)
    fig, ax = plt.subplots(figsize=figsize)
    disp.plot(ax=ax)
    plt.title(f'AP Score: {ap:.2%}')
    plt.show()
    
# roc curve 시각화 함수
def plot_roc_curve(y, pos_proba, title=None, figsize=(6, 6)):
    from sklearn.metrics import roc_curve, roc_auc_score, RocCurveDisplay
    fpr, tpr, _ = roc_curve(y, pos_proba)
    auc = roc_auc_score(y, pos_proba)
    disp = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auc, estimator_name=title)
    fig, ax = plt.subplots(figsize=figsize)
    disp.plot(ax=ax)
    plt.title(f'AUC Score: {auc:.2%}')
    plt.show()

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
    # acc_prec_ax.set_title('Accuracy & Precision')
    acc_prec_ax.set_ylabel('Score')
    # precision accuracy 퍼센트로 표시
    acc_prec_ax.text(0, acc*100, f'{acc*100:.2f}%', ha='center', va='bottom')
    acc_prec_ax.text(1, prec*100, f'{prec*100:.2f}%', ha='center', va='bottom')
    
    # recall ax에 가로 바차트로 spec, recall 표시-> 'Recall', 'Specificity' 표시는 세로로
    rc = recall_score(y_true, y_pred)
    spec = cm[0, 0] / (cm[0, 0] + cm[0, 1])
    recall_ax.barh(['Recall', 'Specificity'], [rc*100, spec*100], color=color)
    recall_ax.set_xlim(0, 100)
    # recall_ax.set_title('Specificity & Recall')
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

# disp 비교함수
def compare_disp(disp1, disp2, figsize=(6, 6), title=None):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=figsize)
    disp1.plot(ax=ax)
    disp2.plot(ax=ax)
    if title:
        plt.title(title)
    plt.show()
    
# roc curve 비교
def compare_roc(y, pos_proba1, pos_proba2, title1=None, title2=None, figsize=(6, 6)):
    from sklearn.metrics import roc_curve, roc_auc_score, RocCurveDisplay
    
    fpr1, tpr1, _ = roc_curve(y, pos_proba1)
    auc1 = roc_auc_score(y, pos_proba1)
    disp1 = RocCurveDisplay(fpr=fpr1, tpr=tpr1, roc_auc=auc1, estimator_name=title1)
    
    fpr2, tpr2, _ = roc_curve(y, pos_proba2)
    auc2 = roc_auc_score(y, pos_proba2)
    disp2 = RocCurveDisplay(fpr=fpr2, tpr=tpr2, roc_auc=auc2, estimator_name=title2)
    
    compare_disp(disp1, disp2, figsize=figsize, title='ROC Curve')

# pr curve 비교
def compare_pr(y, pos_proba1, pos_proba2, title1=None, title2=None, figsize=(6, 6)):
    from sklearn.metrics import precision_recall_curve, average_precision_score, PrecisionRecallDisplay
    
    prec1, rec1, _ = precision_recall_curve(y, pos_proba1)
    ap1 = average_precision_score(y, pos_proba1)
    disp1 = PrecisionRecallDisplay(precision=prec1, recall=rec1, average_precision=ap1, estimator_name=title1)
    
    prec2, rec2, _ = precision_recall_curve(y, pos_proba2)
    ap2 = average_precision_score(y, pos_proba2)
    disp2 = PrecisionRecallDisplay(precision=prec2, recall=rec2, average_precision=ap2, estimator_name=title2)
    
    compare_disp(disp1, disp2, figsize=figsize, title='PR Curve')

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
