package com.example.mysql.dto;

import lombok.Data;

@Data
public class MenuDto extends ExpandCondition {
    /** 主键ID */
    private Integer id;

    /** 应用 */
    private String application;

    /** 组织 */
    private String compGroup;

    /** 名称 */
    private String menuCode;

    /** 名称 */
    private String menuName;

    /** 菜单层级 */
    private String menuLevel;

    /** 父菜单ID */
    private String parentId;

    /** 静态页面连接 */
    private String htmlUrl;

    /** 动态链接 */
    private String serverUrl;

    /** vue链接 */
    private String vueUrl;

    /** 参数 */
    private String appParam;

    /** 图标 */
    private String icon;

    /** 图标图片地址 */
    private String iconUrl;

    /** 显示开关 */
    private String disableFlag;

    /** 排序 */
    private Integer itemSort;


}
