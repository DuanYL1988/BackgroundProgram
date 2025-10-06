package com.example.mysql.dto;

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

    private String type;

    public String getSelectQuary() {
        return selectQuary;
    }

    public void setSelectQuary(String selectQuary) {
        this.selectQuary = selectQuary;
    }

    public String getJoinPart() {
        return joinPart;
    }

    public void setJoinPart(String joinPart) {
        this.joinPart = joinPart;
    }

    public String getCondition() {
        return condition;
    }

    public void setCondition(String condition) {
        this.condition = condition;
    }

    public String getOrderBy() {
        return orderBy;
    }

    public void setOrderBy(String orderBy) {
        this.orderBy = orderBy;
    }

    public String getGroupBy() {
        return groupBy;
    }

    public void setGroupBy(String groupBy) {
        this.groupBy = groupBy;
    }

    public String getHaving() {
        return having;
    }

    public void setHaving(String having) {
        this.having = having;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getPageSize() {
        return pageSize;
    }

    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }

    public int getPageNo() {
        return pageNo;
    }

    public int getStartRow() {
        return startRow;
    }

    public void setStartRow(int startRow) {
        this.startRow = startRow;
    }

    public void setPageNo(int pageNo) {
        this.pageNo = pageNo;
    }

    public long getMaxPage() {
        return maxPage;
    }

    public void setMaxPage(long maxPage) {
        this.maxPage = maxPage;
    }

    public String getActionName() {
        return actionName;
    }

    public void setActionName(String actionName) {
        this.actionName = actionName;
    }

}
