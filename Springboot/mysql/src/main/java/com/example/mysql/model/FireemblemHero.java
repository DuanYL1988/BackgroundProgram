package com.example.mysql.model;

import lombok.Data;

@Data
public class FireemblemHero{
    /** 主键ID */
    private String id;

    /** 称号 */
    private String titleName;

    /** 名 */
    private String name;

    /** 中文名 */
    private String nameCn;

    /** 日文名 */
    private String nameJp;

    /** 立绘图片文件夹名 */
    private String imgName;

    /** 头像 */
    private String faceImg;

    /** 状态立绘 */
    private String stageImg;

    /** 插入立绘 */
    private String cutInImg;

    /** 地图人物图片 */
    private String spriteImg;

    /** 关联立绘 */
    private String artImg;

    /** 稀有度 */
    private String rarity;

    /** 生命 */
    private Integer hp;

    /** 攻击 */
    private Integer atk;

    /** 速度 */
    private Integer spd;

    /** 防御 */
    private Integer def;

    /** 魔防 */
    private Integer res;

    /** 祝福 */
    private String blessing;

    /** 类型 */
    private String heroType;

    /** 兵种 */
    private String moveType;

    /** 武器名 */
    private String weapon;

    /** 武器类型 */
    private String weaponType;

    /** 武器攻击力 */
    private Integer weaponPower;

    /** 角色作品 */
    private String entry;

    /** 宝珠颜色 */
    private String color;

    /** 种族 */
    private String race;

    /** A技能 */
    private String skillA;

    /** B技能 */
    private String skillB;

    /** C技能 */
    private String skillC;

    /** 辅助技能 */
    private String skillAss;

    /** 必杀技 */
    private String skillSp;

    /** 突破极限 */
    private Integer limitPlus;

    /** 神龙之花 */
    private Integer dragonFlower;

    /** 喜欢 */
    private String favorite;

    /** 评价等级 */
    private String heroRank;

    /** 抽中flag */
    private String pickFlag;

    /** 登录日期 */
    private String releaseDate;
}
