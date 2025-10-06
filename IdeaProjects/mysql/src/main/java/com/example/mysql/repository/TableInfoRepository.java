package com.example.mysql.repository;

import java.util.List;

import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.mysql.dto.TableInfoDto;
import com.example.mysql.model.TableInfo;

/**
 * 数据库表管理Repository
 */
@Repository
public interface TableInfoRepository {

    /**
     * 业务主键查找唯一值
     *
     * @Param  {id} ID
     * @Return 数据库表管理记录
     */
    TableInfo selectOneByUniqueKey(@Param("tableName") String tableName, @Param("colName") String colName);

    /**
     * 根据条件取得件数
     *
     * @Param  {condition} 检索条件
     * @Return 记录数
     */
    int getCountByDto(TableInfoDto condition);

    /**
     * 根据条件取得一览
     *
     * @Param  {condition} 检索条件
     * @Return 数据库表管理记录List
     */
    List<TableInfo> selectByDto(TableInfoDto condition);

    /**
     * 新增一条数据
     *
     * @Param  {TableInfo 实体Pojo
     * @Return 0:失败,1:成功
     */
    int insert(TableInfo model);

    /**
     * 更新一条数据
     *
     * @Param  {TableInfo 实体Pojo
     * @Return 更新件数
     */
    int update(TableInfo model);

    /**
     * 自定义查询
     *
     * @Param  {condition} 扩展字段实现自定义SQL查询
     * @Return 数据库表管理记录List
     */
    List<TableInfo> customQuary(TableInfoDto condition);

}
