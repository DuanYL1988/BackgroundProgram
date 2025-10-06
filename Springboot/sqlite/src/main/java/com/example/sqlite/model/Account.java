package com.example.sqlite.model;

import lombok.Data;

@Data
public class Account extends ExpandCondition {

    /**
     * '涓婚敭'
     */
    private Integer id;

    /**
     * '鐢ㄦ埛鍚�'
     */
    private String loginName;

    /**
     * '鐢ㄦ埛鍚�'
     */
    private String username;

    /**
     * '瀵嗙爜'
     */
    private String password;

    /**
     * '鏉冮檺'
     */
    private String roleId;

    /**
     * '搴旂敤'
     */
    private String application;

    /**
     * '鍏徃'
     */
    private String company;

    /**
     * '缁勭粐'
     */
    private String groupName;

    /**
     * '鐢佃瘽'
     */
    private String telphone;

    /**
     * '澶村儚(鏈湴)'
     */
    private String faceLocal;

    /**
     * '澶村儚鍦板潃'
     */
    private String faceUrl;

    private String token;
}
