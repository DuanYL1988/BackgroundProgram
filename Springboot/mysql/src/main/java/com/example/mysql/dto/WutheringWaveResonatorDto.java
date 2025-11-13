package com.example.mysql.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class WutheringWaveResonatorDto extends ExpandCondition {
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

    /** 卡片立绘 */
    private String cardImg;

    /** 编队立绘 */
    private String spriteImg;

    /** 海报立绘 */
    private String postImg;

    /** 稀有度 */
    private String rarity;

    /** 属性 */
    private String attrs;

    /** 武器属性 */
    private String weaponType;

    /** 词缀 */
    private String tags;

    /** 势力 */
    private String influence;

    /** 出生地 */
    private String birthPlace;

    /** 生命 */
    private String hp;

    /** 攻击 */
    private String atk;

    /** 防御 */
    private String def;

    /** 技能 */
    private String skills;

    /** 技能图标 */
    private String skillsIcon;

    /** 艺术集 */
    private String artworks;

    /** YT视频 */
    private String ytVideos;

    /** YT短视频 */
    private String shortVideos;

    /** 表情包 */
    private String emoji;

    /** 版本 */
    private String version;

    /** 实装日期 */
    private String releaseDate;


}
