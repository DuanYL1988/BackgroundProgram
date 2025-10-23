package com.example.mysql.model;

import lombok.Data;

@Data
public class TableInfo {
    /** 表名 */
    private String tableName;

    /** 字段名 */
    private String colName;

    /** 字段名中文 */
    private String colNameCh;

    /** 字段驼峰 */
    private String colCamel;

    /** 字段属性 */
    private String colType;

    /** 长度 */
    private String colLength;

    /** 主键flag */
    private String colPkFlg;

    /** 非空flag */
    private String colNotnullFlg;

    /** 业务逻辑主键 */
    private String colUniqueFlg;

    /** 输入类型 */
    private String colInputtype;

    /** 新建flag */
    private String colInsertable;

    /** 字段更新flag */
    private String colUpdateable;

    /** 检索条件flag */
    private String colFifterable;

    /** 表示flag */
    private String colDisableFlg;

    /** 一览表示flag */
    private String colListDisableFlag;

    /** 一览宽度 */
    private String colListWidth;

    /** 输入宽度 */
    private String colInputWidth;

    /** 排序 */
    private String colSort;

    /** 类型Code */
    private String colCode;

    /** 默认值 */
    private String colDefault;


}
