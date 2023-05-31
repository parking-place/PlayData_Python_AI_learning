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
    import seaborn as sns
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=figsize)
    if title is not None:
        fig.suptitle(title, fontsize=16)
    axs = fig.subplots(2, 2)
    cm_ax, recall_ax = axs[0]
    acc_prec_ax, f1_ax = axs[1]
    # 혼동행렬 생성
    tags= ['TN', 'FP', 'FN', 'TP']
    counts = [f'{value:0.0f}' for value in confusion_matrix(y_true, y_pred).flatten()]
    labels = [f'{t}\n{c}' for t, c in zip(tags, counts)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(confusion_matrix(y_true, y_pred),
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
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
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
