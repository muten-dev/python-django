import pandas as pd

from titanic.models.dataset import Dataset
from titanic.models.service import Service
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


class Controller(object):

    dataset = Dataset()
    service = Service()

    def modeling(self, train, test) -> object:
        service = self.service
        this = self.preprocess(train, test)
        this.label = service.create_label(this)
        this.train = service.create_train(this)
        return this

    def learning(self, train, test):
        this = self.modeling(train, test)
        print(f'사이킷런의 SVC 알고리즘 정확도 {self.service.accuracy_by_svm(this)} %')

    def submit(self, train, test):
        this = self.modeling(train, test)
        clf = RandomForestClassifier()
        clf.fit(this.train, this.label)
        prediction = clf.predict(this.test)
        pd.DataFrame({'PassengerId': this.id, 'Survived': prediction}).to_csv('./data/submission.csv', index=False)

    def preprocess(self, train, test) -> object:
        service = self.service
        this = self.dataset
        # 초기 모델 생성
        this.train = service.new_model(train)
        this.test = service.new_model(test)
        this.id = this.test['PassengerId']

        # nominal, ordinal 로 데이터 정형화
        this = service.embarked_nominal(this)
        this = service.title_nominal(this)
        this = service.gender_nominal(this)
        this = service.age_ordinal(this)
        this = service.fare_ordinal(this)

        # 불필요한 feature (Cabin, Ticket, Name, Sex) 제거
        # feature = ['Cabin', 'Ticket', 'Name', 'Sex']
        this = service.drop_feature(this, 'Cabin', 'Ticket', 'Name',
                                    'Sex', 'Age', 'Fare')
        self.print_this(this)
        return this

    @staticmethod
    def print_this(this):
        print('*' * 100)
        print(f'1. Train 의 type\n {type(this.train)}')
        print(f'2. Train 의 column\n {this.train.columns}')
        print(f'3. Train 의 상위 1개 행\n {this.train.head(5)}')
        print(f'4. Train 의 null 의 개수\n {this.train.isnull().sum()}')
        # print(this.train['Title'])
        print(f'5. Test 의 type\n {type(this.test)}')
        print(f'6. Test 의 column\n {this.test.columns}')
        print(f'7. Test 의 상위 1개 행\n {this.test.head(5)}')
        print(f'8. Test 의 null 의 개수\n {this.test.isnull().sum()}')
        print('*' * 100)
