package com.example.mysql.dto;

import lombok.Data;

@Data
public class ArknightsOperatorDto extends ExpandCondition {
    /** 主键 */
    private String id;

    /** 英文名 */
    private String name;

    /** 中文名 */
    private String nameCn;

    /** 日文名 */
    private String nameJp;

    /** 头像 */
    private String faceImg;

    /** 精1立绘 */
    private String stageOneImg;

    /** 精2立绘 */
    private String stageTwoImg;

    /** 地图人物图片 */
    private String spriteImg;

    /** 皮肤名称 */
    private String skinName;

    /** 皮肤头像 */
    private String skinIcon;

    /** 皮肤战斗图片 */
    private String skinSprite;

    /** 皮肤立绘 */
    private String skinImage;

    /** 默认皮肤 */
    private String defaltSkin;

    /** 稀有度 */
    private String rarity;

    /** 职业 */
    private String vocation;

    /** 副职业 */
    private String subVocation;

    /** 词缀 */
    private String tags;

    /** 势力 */
    private String influence;

    /** 出生地 */
    private String birthPlace;

    /** 种族 */
    private String race;

    /** 生命 */
    private String hp;

    /** 攻击 */
    private String atk;

    /** 防御 */
    private String def;

    /** 法抗 */
    private String res;

    /** 部署费用 */
    private String cost;

    /** 技能 */
    private String skills;

    /** 技能图标 */
    private String skillsIcon;

    /** 基建技能 */
    private String buildSkills;

    /** 潜能 */
    private String capacity;

    /** 实装日期 */
    private String releaseDate;


}
