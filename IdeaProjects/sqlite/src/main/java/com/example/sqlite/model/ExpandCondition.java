package com.example.sqlite.model;

import lombok.Data;

@Data
public class ExpandCondition {

    /**
     * SQL select部
     */
    private String selectQuary;

    /**
     * SQL join部
     */
    private String joinPart;

    /**
     * SQL where部
     */
    private String condition;

    /**
     * SQL order部
     */
    private String orderBy;

    /**
     * SQL group部
     */
    private String groupBy;

    /**
     * SQL having部
     */
    private String having;

    /**
     * 每页显示几个
     */
    private int pageSize = 500;

    /**
     * 当前页数
     */
    private int pageNo = 1;

    /**
     * 开始行
     */
    private int startRow = 0;

    /**
     * 最大页数
     */
    private long maxPage;

    /**
     * 查询出件数
     */
    private int count;

    /**
     * 操作名
     */
    private String actionName;

}
