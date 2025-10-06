package com.example.sqlite.model;

import lombok.Data;

@Data
public class Menu extends ExpandCondition {
    /**
     * 主键
     */
    private Integer id;

    /**
     * 应用
     */
    private String application;

    /**
     * 公司
     */
    private String company;

    /**
     * 组织
     */
    private String compGroup;

    /**
     * 位置
     */
    private String location;

    /**
     * 名称
     */
    private String name;

    /**
     * 静态页面连接
     */
    private String htmlUrl;

    /**
     * 动态链接
     */
    private String serverUrl;

    /**
     * 链接
     */
    private String vueUrl;

    /**
     * 图标
     */
    private String iconUrl;

    /**
     * 排序
     */
    private Integer sort;
}
