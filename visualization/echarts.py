# /user/bin/python
# coding=utf-8
from pyecharts.charts import Page, Pie, Bar, WordCloud, Scatter, Funnel
from pyecharts import options as opts
from pyecharts.globals import SymbolType, ThemeType
import random


class charts():
    # 条形图
    def bar(self, key, value, city, title, subtitle) -> Bar:
        theme = [
            ThemeType.LIGHT, ThemeType.DARK, ThemeType.WHITE, ThemeType.CHALK,
            ThemeType.ESSOS, ThemeType.INFOGRAPHIC, ThemeType.MACARONS, ThemeType.PURPLE_PASSION,
            ThemeType.ROMA, ThemeType.ROMANTIC, ThemeType.SHINE, ThemeType.VINTAGE,
            ThemeType.WALDEN, ThemeType.WESTEROS, ThemeType.WONDERLAND
        ]
        c = (
            Bar(init_opts=opts.InitOpts(theme=random.choice(theme)))
                .add_xaxis(key)
                .add_yaxis(city, value)
                .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=subtitle),
                                 toolbox_opts=opts.ToolboxOpts(),
                                 legend_opts=opts.LegendOpts(is_show=False)
                                 )
        )
        return c

    # 饼图
    def pie(self, key, value, title) -> Pie:
        c = (
            Pie()
                .add("", [list(z) for z in zip(key, value)])
                .set_global_opts(title_opts=opts.TitleOpts(title=title))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c

    def pie_radius(self, key, value, title) -> Pie:
        c = (
            Pie()
                .add("", [list(z) for z in zip(key, value)], radius=["40%", "75%"],
                     )
                .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                legend_opts=opts.LegendOpts(
                    orient="vertical", pos_top="15%", pos_left="2%"
                ),
            )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c

    # 玫瑰饼图
    def pie_rosetype(self, key, value, title) -> Pie:
        v = key
        c = (
            Pie()
                .add("", [list(z) for z in zip(v, value)], radius=["30%", "75%"], center=["50%", "50%"],
                     rosetype="area",
                     ).set_global_opts(title_opts=opts.TitleOpts(title=title))
        )
        return c

    # 词云图
    def wordcloud_diamond(self, word, title) -> WordCloud:
        shape = [SymbolType.ARROW, SymbolType.DIAMOND, SymbolType.RECT, SymbolType.ROUND_RECT, SymbolType.TRIANGLE]
        c = (
            WordCloud()
                .add("", word, word_size_range=[20, 100], shape=random.choice(shape))
                .set_global_opts(title_opts=opts.TitleOpts(title=title))
        )
        return c

    # 散点图显示分割线
    def scatter_spliteline(self, key, value, city, title) -> Scatter:
        c = (
            Scatter()
                .add_xaxis(key)
                .add_yaxis(city, value)
                .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            )
        )
        return c

    def scatter_visualmap_color(self, key, value, city, title) -> Scatter:
        c = (
            Scatter()
                .add_xaxis(key)
                .add_yaxis(city, value)
                .set_global_opts(title_opts=opts.TitleOpts(title=title),
                                 visualmap_opts=opts.VisualMapOpts(type_="size", max_=150, min_=20),
                                 )
        )
        return c

    # 漏斗图
    def funnel_label_inside(self, key, value, title) -> Funnel:
        c = (
            Funnel()
                .add("租房", [list(z) for z in zip(key, value)], label_opts=opts.LabelOpts(position="inside"),
                     ).set_global_opts(title_opts=opts.TitleOpts(title=title))
        )
        return c
