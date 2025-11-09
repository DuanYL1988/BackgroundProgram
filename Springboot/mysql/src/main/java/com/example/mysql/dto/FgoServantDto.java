package com.example.mysql.dto;

import lombok.Data;

@Data
public class FgoServantDto extends ExpandCondition {
    /** ID */
    private String id;

    /** 英文名 */
    private String name;

    /** 中文名 */
    private String nameCn;

    /** 日文名 */
    private String nameJp;

    /** 立绘图片文件夹名 */
    private String imgName;

    /** 职介 */
    private String classType;

    /** 稀有度 */
    private String rarity;

    /** 从者类型(拐,打手) */
    private String heroType;

    /** 性别 */
    private String gender;

    /** 属性 */
    private String attrs;

    /** 副属性 */
    private String subAttrs;

    /** 特性 */
    private String traits;

    /** 生命值 */
    private Integer hp;

    /** 攻击 */
    private Integer attact;

    /** 活动从者 */
    private String eventFlag;

    /** 1技能 */
    private String skill1;

    /** 2技能 */
    private String skill2;

    /** 3技能 */
    private String skill3;

    /** 宝具名 */
    private String skillExtra;

    /** 宝具类型(单体,全体) */
    private String extraType;

    /** 宝具颜色 */
    private String extraColor;

    /** 头像URL */
    private String faceImg;

    /** 默认状态 */
    private Integer defaultStage;

    /** 普通立绘 */
    private String stageImg;

    /** 灵衣立绘 */
    private String skinImg;

    /** 状态名集合 */
    private String stageNameList;

    /** 地图人物图片 */
    private String spriteImg;

    /** 头像图标立绘 */
    private String iconImg;

    /** 组队立绘 */
    private String formationImg;

    /** 表情集 */
    private String expressionSheets;

    /** 相关礼装 */
    private String craftEssences;

    /** 艺术集 */
    private String artworks;

    /** 立绘集 */
    private String illustrations;

    /** 表情包 */
    private String emoji;

    /** 评价等级 */
    private String heroRank;

    /** 抽中flag */
    private String pickFlag;

    /** 登录日期 */
    private String releaseDate;


}
