package com.example.mysql.dto;

import lombok.Data;

@Data
public class AccountDto extends ExpandCondition {
    /** 主键 */
    private Integer id;

    /** 用户名 */
    private String loginName;

    /** 用户名 */
    private String username;

    /** 密码 */
    private String password;

    /** 权限 */
    private String roleId;

    /** 应用 */
    private String application;

    /** 公司 */
    private String company;

    /** 组织 */
    private String groupName;

    /** 电话 */
    private String telphone;

    /** 头像(本地) */
    private String faceLocal;

    /** 头像地址URL */
    private String faceUrl;


}
