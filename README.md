# EventRecommendation


## 数据

数据来源于Kaggle竞赛：Event Recommendation Engine Challenge，根据 events they’ve responded to in the past user demographic information what events they’ve seen and clicked on in our app 用户对某个活动是否感兴趣。

## 模型

根据协同过滤算法原理，采用3种算法预测用户是否对活动感兴趣：

（1）基于用户的协同过滤，计算两个用户之间的相似度，根据历史参加活动的用户与当前用户的相似度，预测用户对活动的评分（用户本身关系，用户好友分析）；

（2）基于活动的协同过滤，计算两个活动之间的相似度，根据用户历史参加活动与当前活动的相似度，预测用户对活动的评分（活动本身关系，用户活动关联分析）；

（3）基于模型的协同过滤，通过对评分矩阵进行降维和梯度下降，并调整正则参数，预测用户对活动的评分。

