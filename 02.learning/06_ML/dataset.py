# 트레인 테스트 데이터셋 분리 모듈
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def get_boston_dataset(test_size=0.25, path=r'./data/boston_hosing.csv', random_state=1473032201):
    df = pd.read_csv(path)
    X = df.drop('MEDV', axis=1)
    y = df['MEDV']
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=test_size,
                                                        random_state=random_state,
                                                        )
    return X_train, X_test, y_train, y_test

def get_wine_dataset(test_size=0.25, path=r'./data/wine.csv', random_state=1473032201):
    df = pd.read_csv(path)
    X = df.drop('color', axis=1)
    y = df['color']
    le = LabelEncoder()
    le.fit(['A', 'B', 'C'])
    X['quality'] = le.transform(X['quality'])    
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=test_size,
                                                        stratify=y,
                                                        random_state=random_state,
                                                        )
    return X_train, X_test, y_train, y_test

def get_breast_cancer_dataset(test_size=0.25, random_state=1473032201, scaling=False):
    """
    [param]
        scaling: bool - 스케일링 여부
    [return]
        Tuple : ((X_train, X_test, y_train, y_test), feature_names)
    """
    from sklearn.datasets import load_breast_cancer
    X, y = load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        stratify=y,
                                                        test_size=test_size,
                                                        random_state=random_state,
                                                        )
    
    if scaling:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    
    feature_names = load_breast_cancer()['feature_names']
    
    return ((X_train, X_test, y_train, y_test), feature_names)
