package com.example.sqlite.model;

import java.util.Date;

public class TableInfo extends ExpandCondition {
    /**
     * 主键
     */
    private Integer id;

    /**
     * 表名
     */
    private String tableName;

    /**
     * 字段名
     */
    private String colName;

    /**
     * 字段名中文
     */
    private String colNameCh;

    /**
     * 字段驼峰
     */
    private String colJavaName;

    /**
     * 字段属性
     */
    private String colType;

    /**
     * 长度
     */
    private Integer colLength;

    /**
     * 主键
     */
    private Integer colPkFlg;

    /**
     * 非空
     */
    private Integer colNotnullFlg;

    /**
     * 输入类型
     */
    private String colInputtype;

    /**
     * 新建
     */
    private Integer colInsertable;

    /**
     * 字段更新
     */
    private Integer colUpdateable;

    /**
     * 检索条件
     */
    private Integer colFifterable;

    /**
     * 表示
     */
    private Integer colDisableFlg;

    /**
     * 一览表示
     */
    private Integer colListDisableFlag;

    /**
     * 对应
     */
    private String colCode;

    /**
     * 设定主键
     */
    public void setId(Integer id){
        this.id = id;
    }

    /**
     * 取得主键
     */
    public Integer getId(){
        return id;
    }

    /**
     * 设定表名
     */
    public void setTableName(String tableName){
        this.tableName = tableName;
    }

    /**
     * 取得表名
     */
    public String getTableName(){
        return tableName;
    }

    /**
     * 设定字段名
     */
    public void setColName(String colName){
        this.colName = colName;
    }

    /**
     * 取得字段名
     */
    public String getColName(){
        return colName;
    }

    /**
     * 设定字段名中文
     */
    public void setColNameCh(String colNameCh){
        this.colNameCh = colNameCh;
    }

    /**
     * 取得字段名中文
     */
    public String getColNameCh(){
        return colNameCh;
    }

    /**
     * 设定字段驼峰
     */
    public void setColJavaName(String colJavaName){
        this.colJavaName = colJavaName;
    }

    /**
     * 取得字段驼峰
     */
    public String getColJavaName(){
        return colJavaName;
    }

    /**
     * 设定字段属性
     */
    public void setColType(String colType){
        this.colType = colType;
    }

    /**
     * 取得字段属性
     */
    public String getColType(){
        return colType;
    }

    /**
     * 设定长度
     */
    public void setColLength(Integer colLength){
        this.colLength = colLength;
    }

    /**
     * 取得长度
     */
    public Integer getColLength(){
        return colLength;
    }

    /**
     * 设定主键
     */
    public void setColPkFlg(Integer colPkFlg){
        this.colPkFlg = colPkFlg;
    }

    /**
     * 取得主键
     */
    public Integer getColPkFlg(){
        return colPkFlg;
    }

    /**
     * 设定非空
     */
    public void setColNotnullFlg(Integer colNotnullFlg){
        this.colNotnullFlg = colNotnullFlg;
    }

    /**
     * 取得非空
     */
    public Integer getColNotnullFlg(){
        return colNotnullFlg;
    }

    /**
     * 设定输入类型
     */
    public void setColInputtype(String colInputtype){
        this.colInputtype = colInputtype;
    }

    /**
     * 取得输入类型
     */
    public String getColInputtype(){
        return colInputtype;
    }

    /**
     * 设定新建
     */
    public void setColInsertable(Integer colInsertable){
        this.colInsertable = colInsertable;
    }

    /**
     * 取得新建
     */
    public Integer getColInsertable(){
        return colInsertable;
    }

    /**
     * 设定字段更新
     */
    public void setColUpdateable(Integer colUpdateable){
        this.colUpdateable = colUpdateable;
    }

    /**
     * 取得字段更新
     */
    public Integer getColUpdateable(){
        return colUpdateable;
    }

    /**
     * 设定检索条件
     */
    public void setColFifterable(Integer colFifterable){
        this.colFifterable = colFifterable;
    }

    /**
     * 取得检索条件
     */
    public Integer getColFifterable(){
        return colFifterable;
    }

    /**
     * 设定表示
     */
    public void setColDisableFlg(Integer colDisableFlg){
        this.colDisableFlg = colDisableFlg;
    }

    /**
     * 取得表示
     */
    public Integer getColDisableFlg(){
        return colDisableFlg;
    }

    /**
     * 设定一览表示
     */
    public void setColListDisableFlag(Integer colListDisableFlag){
        this.colListDisableFlag = colListDisableFlag;
    }

    /**
     * 取得一览表示
     */
    public Integer getColListDisableFlag(){
        return colListDisableFlag;
    }

    /**
     * 设定对应
     */
    public void setColCode(String colCode){
        this.colCode = colCode;
    }

    /**
     * 取得对应
     */
    public String getColCode(){
        return colCode;
    }


}
