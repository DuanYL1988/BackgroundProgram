package com.example.mysql.dto;

import lombok.Data;

/**
 * 单表特定字段批量更新用Model
 */
@Data
public class BatchColumnDto{
    // 更新对象表名
    private String tableName;
    // 更新对象字段名
    private String tgtColNm;
    // 更新对象条件字段字段名
    private String condColNm;
    // 条件列集合
    private String[] ids;
    // 更细值集合
    private String[] values;
}
