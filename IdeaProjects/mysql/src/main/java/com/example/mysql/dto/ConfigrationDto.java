package com.example.mysql.dto;

import lombok.Data;

@Data
public class ConfigrationDto extends ExpandCondition {
    /** 实体名 */
    private String tableName;

    /** 主页URL */
    private String baseUrl;

    /** 图片URL */
    private String imgUrl;

    /** 一览URL */
    private String listUrl;

    /** 爬虫请求间隔 */
    private Integer waitTime;

    /** 替换关键字 */
    private String replaceKeyword;

    /** 图片下载目录 */
    private String localDirectory;


}
