- 链家房产数据爬取分析可视化平台(之前实习时候写的，实习时候整天9116没时间，为了应付毕设，代码太辣眼睛了，最近在重构，准备封装成mysql+mongo+es，欢迎给我提issue，互相学习O(∩_∩)O~~)
    - 该平台主要分为三个模块
        - 数据爬取模块
        * 使用scrapy框架对链家的新房，二手房，租房数据进行爬取，存入MongoDB和Elasticsearch数据库
        *  data_visualize模块聚合MongoDB进行数据分析后，利用pyecharts生成图表保存到本地
        * 通过flask实现数据的网站展示
---
## notes: The project is under refactor
### todo
#### refactor website with django
#### refactor database with mysql and mongodb 

+ 项目运行步骤：
+ 安装依赖的python包
+ pip install -r requirements.txt
+ 运行GraduationProject目录的run.py,即可运行项目
+ data_visualize目录为数据分析模块代码
+ lianjia为网站显示模块
+ spider为爬虫模块
+ config目录为项目的配置文件
---
+ 数据分析视角
---
+ 新房
    1. main_price各区间分布
    2. second_price各区间分布
    3. 每平米均价
    4. 每套均价
    5. 每平米最贵top5
    6. 每平最低top5
    7. 物业类型占比分布
    8. 户型分布情况
    9. tag词云

---

+ 二手房
    * 每平米均价
    * 每套均价
    * 每平米价格区间分布
    * 每套价格区间分布
    * 每平米最贵top5
    * 每套最贵top5
    * 小区名词云
    * position词云
---
+ 租房
    * 每个品牌房源占比
    * 每套房租房均价
    * 每套最贵top5
    * 每套最低top5
    * tag词云
---
+ 数据可视化模块通过pyecharts读取数据进行图表渲染
## 数据可视化图表如下:
* 二手房

![](lianjia/static/ershoufang/avg_loupan/新一线城市二手房每套均价(1).gif)
![](lianjia/static/ershoufang/position_wordcloud/北京市二手房热门地段.gif)
![](lianjia/static/ershoufang/square_meter_max_top5/北京市二手房每平米最贵top5小区.gif)
![](lianjia/static/ershoufang/square_meter_min_top5/哈尔滨市二手房每平米最便宜top5小区.gif)
![](lianjia/static/ershoufang/total_price_range/成都市二手房每套房价位占比分布图.gif)
![](lianjia/static/ershoufang/unit_price_range/北京市二手房每平米楼盘价位占比分布图.gif)
![](lianjia/static/ershoufang/xiaoqu_wordcloud/武汉市二手房热门小区.gif)

* 新房
![](lianjia/static/newhouse/avg_loupan/链家部分二线内陆城市每套新房均价.gif)
![](lianjia/static/newhouse/avg_square_meter/链家部分一线城市及新一线城市新房每平米均价.gif)
![](lianjia/static/newhouse/huxing_count/珠海市新房户型占比分布图.gif)
![](lianjia/static/newhouse/main_price_range/承德市新房每平米楼盘价位占比分布图.gif)
![](lianjia/static/newhouse/second_price_range/重庆市每套新房价位占比分布图.gif)
![](lianjia/static/newhouse/square_meter_max_top5/成都市新房每平米最贵top5楼盘.gif)
![](lianjia/static/newhouse/square_meter_min_top5/杭州市新房每平米最便宜top5楼盘.gif)
![](lianjia/static/newhouse/tag_wordcloud/上海市新房热门标签.gif)
![](lianjia/static/newhouse/wuye_type_count/南京市新房物业类型占比分布图.gif)
* 租房
  ![](lianjia/static/rent/avg_price/一线城市租房均价.gif)
  ![](lianjia/static/rent/brand_avg_price/东莞市房源占比最高平台top5均价.gif)
  ![](lianjia/static/rent/rent_max_top5/合肥市租房价格最高top5.gif)
  ![](lianjia/static/rent/rent_min_top5/杭州市租房价格最低top5.gif)
  ![](lianjia/static/rent/source_percentage/广州市链家租房来源.gif)
  ![](lianjia/static/rent/tag_wordcloud/杭州市租房热门标签.gif)

  ##### 本源码只作技术交流使用，请勿用以违法用途，由本源码直接或间接产生的法律问题，将由使用者自行承担
