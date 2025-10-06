package com.example.mysql.dto;

import lombok.Data;

@Data
public class CodeMasterDto extends ExpandCondition {
    /** 主键 */
    private Integer id;

    /** 应用 */
    private String application;

    /** 种类ID */
    private String categoryId;

    /** 种类名 */
    private String categoryName;

    /** code */
    private String code;

    /** 名 */
    private String name;

    /** 链接 */
    private String linkUrl;

    /** 图片地址 */
    private String imgUrl;

    /** 用户权限组 */
    private String roleGroup;

    /** 关联父种类 */
    private String parentId;

    /** 扩展字段1 */
    private String memo1;

    /** 扩展字段2 */
    private String memo2;

    /** 扩展字段3 */
    private String memo3;

    /** 扩展数字字段1 */
    private Integer numberCol1;

    /** 扩展数字字段2 */
    private Integer numberCol2;

    /** 扩展数字字段3 */
    private Integer numberCol3;


}
