package com.example.sqlite.model;

import lombok.Data;

import java.util.Date;

@Data
public class Servant extends ExpandCondition {
    /**
     * 
     */
    private String id;

    /**
     * 立绘图片文件夹名
     */
    private String imgName;

    /**
     * 名
     */
    private String name;

    /**
     * 昵称
     */
    private String nickName;

    /**
     * 兵种
     */
    private String classType;

    /**
     * 从者类型(拐,打手)
     */
    private String heroType;

    /**
     * 活动从者
     */
    private String eventFlag;

    /**
     * 生命值
     */
    private Integer hp;

    /**
     * 攻击
     */
    private Integer attact;

    /**
     * 1技能
     */
    private String skill1;

    /**
     * 2技能
     */
    private String skill2;

    /**
     * 3技能
     */
    private String skill3;

    /**
     * 宝具名
     */
    private String skillExtra;

    /**
     * 宝具类型(单体,全体)
     */
    private String extraType;

    /**
     * 宝具颜色
     */
    private String extraColor;

    /**
     * 突破极限
     */
    private Integer limitLevel;

    /**
     * 特性
     */
    private String traits;

    /**
     * 队伍
     */
    private Integer team;

    /**
     * 喜欢
     */
    private String favorite;

    /**
     * 评价等级
     */
    private String rank;

    /**
     * 登录日期
     */
    private Date createDatetime;

    /**
     * 更新日期
     */
    private Date updateDatetime;
}
