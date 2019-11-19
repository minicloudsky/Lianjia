MongoDB聚合
---
- 统计深圳所有房产记录
```sql
db.深圳.aggregate([
{$group:{
    _id:null,
    count:{$sum:1}
    }
}
]
)
```
类似于mysql
```mysql
select count(*) as count from 深圳
```
- 统计深圳表计算所有main_price求和
```mysql
db.深圳.aggregate([
{
        $group:{
            _id:null,
            total:{$sum:"$main_price"}
            }
}
])
```
- 对于每一个唯一的loupan，计算main_price总和
```mysql
db.深圳.aggregate([
{
        $group:{
            _id:"$loupan",
            total:{$sum:"$main_price"}
            }
}
])
```
类似于mysql：
select loupan, sum(price) as total from 深圳,
group by loupan
- 对于每一个唯一的loupan，计算main_price的平均值
```mysql
db.深圳.aggregate([
{
        $group:{
            _id:"$loupan",
            average:{$avg:"$main_price"}
            }
}
])
```
类似于mysql:
select loupan, avg(price) as average from 深圳,
group by loupan
- 对于有多套房在售的楼盘，返回楼盘和对于的数量
```mysql
db.深圳.aggregate([
    {
            $group:{
                    _id:"$loupan",
                    count:{$sum:1}
             }
    },
    {$match:{count:{$gt:1}}}
])
```
类似于mysql中的
select loupan,count(*)
from 深圳
group by loupan
having count(*) > 1
- 对于每一个唯一的wuyetype且loupan='春风十里',
计算main_price总和
```mysql
db.深圳.aggregate([
    { $match  : { loupan: '春风十里'  }  },
    {
            $group:{
                    _id:"$wuyetype",
                    total:{$sum:"$main_price" }
            }
    }
])
```
类似于mysql中:
```mysql
select wuyetype,
    sum(main_price) as total
from 深圳
where loupan='春风十里'
group by wuyetype
```

