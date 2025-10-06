package com.example.sqlite.model;

import java.util.Date;

public class CodeMaster extends ExpandCondition {
    /**
     * 主键
     */
    private Integer id;

    /**
     * 应用
     */
    private String application;

    /**
     * 种类
     */
    private String categoryId;

    /**
     * 种类名
     */
    private String categoryName;

    /**
     * 
     */
    private String code;

    /**
     * 名
     */
    private String name;

    /**
     * 链接
     */
    private String linkUrl;

    /**
     * 图片地址
     */
    private String imgUrl;

    /**
     * 用户权限组
     */
    private String roleGroup;

    /**
     * 关联父种类
     */
    private String parentId;

    /**
     * 扩展字段1
     */
    private String memo1;

    /**
     * 扩展字段2
     */
    private String memo2;

    /**
     * 扩展字段3
     */
    private String memo3;

    /**
     * 扩展数字字段1
     */
    private Integer numberCol1;

    /**
     * 扩展数字字段2
     */
    private Integer numberCol2;

    /**
     * 扩展数字字段3
     */
    private Integer numberCol3;

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
     * 设定应用
     */
    public void setApplication(String application){
        this.application = application;
    }

    /**
     * 取得应用
     */
    public String getApplication(){
        return application;
    }

    /**
     * 设定种类
     */
    public void setCategoryId(String categoryId){
        this.categoryId = categoryId;
    }

    /**
     * 取得种类
     */
    public String getCategoryId(){
        return categoryId;
    }

    /**
     * 设定种类名
     */
    public void setCategoryName(String categoryName){
        this.categoryName = categoryName;
    }

    /**
     * 取得种类名
     */
    public String getCategoryName(){
        return categoryName;
    }

    /**
     * 设定
     */
    public void setCode(String code){
        this.code = code;
    }

    /**
     * 取得
     */
    public String getCode(){
        return code;
    }

    /**
     * 设定名
     */
    public void setName(String name){
        this.name = name;
    }

    /**
     * 取得名
     */
    public String getName(){
        return name;
    }

    /**
     * 设定链接
     */
    public void setLinkUrl(String linkUrl){
        this.linkUrl = linkUrl;
    }

    /**
     * 取得链接
     */
    public String getLinkUrl(){
        return linkUrl;
    }

    /**
     * 设定图片地址
     */
    public void setImgUrl(String imgUrl){
        this.imgUrl = imgUrl;
    }

    /**
     * 取得图片地址
     */
    public String getImgUrl(){
        return imgUrl;
    }

    /**
     * 设定用户权限组
     */
    public void setRoleGroup(String roleGroup){
        this.roleGroup = roleGroup;
    }

    /**
     * 取得用户权限组
     */
    public String getRoleGroup(){
        return roleGroup;
    }

    /**
     * 设定关联父种类
     */
    public void setParentId(String parentId){
        this.parentId = parentId;
    }

    /**
     * 取得关联父种类
     */
    public String getParentId(){
        return parentId;
    }

    /**
     * 设定扩展字段1
     */
    public void setMemo1(String memo1){
        this.memo1 = memo1;
    }

    /**
     * 取得扩展字段1
     */
    public String getMemo1(){
        return memo1;
    }

    /**
     * 设定扩展字段2
     */
    public void setMemo2(String memo2){
        this.memo2 = memo2;
    }

    /**
     * 取得扩展字段2
     */
    public String getMemo2(){
        return memo2;
    }

    /**
     * 设定扩展字段3
     */
    public void setMemo3(String memo3){
        this.memo3 = memo3;
    }

    /**
     * 取得扩展字段3
     */
    public String getMemo3(){
        return memo3;
    }

    /**
     * 设定扩展数字字段1
     */
    public void setNumberCol1(Integer numberCol1){
        this.numberCol1 = numberCol1;
    }

    /**
     * 取得扩展数字字段1
     */
    public Integer getNumberCol1(){
        return numberCol1;
    }

    /**
     * 设定扩展数字字段2
     */
    public void setNumberCol2(Integer numberCol2){
        this.numberCol2 = numberCol2;
    }

    /**
     * 取得扩展数字字段2
     */
    public Integer getNumberCol2(){
        return numberCol2;
    }

    /**
     * 设定扩展数字字段3
     */
    public void setNumberCol3(Integer numberCol3){
        this.numberCol3 = numberCol3;
    }

    /**
     * 取得扩展数字字段3
     */
    public Integer getNumberCol3(){
        return numberCol3;
    }


}
