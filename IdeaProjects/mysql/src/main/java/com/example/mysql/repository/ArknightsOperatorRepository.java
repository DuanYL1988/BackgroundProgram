package com.example.mysql.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.mysql.dto.ArknightsOperatorDto;
import com.example.mysql.model.ArknightsOperator;

/**
 * 明日方舟干员Repository
 */
@Repository
public interface ArknightsOperatorRepository {

    /**
     * 通过ID主键查找唯一一条记录
     * @Param {id} ID
     * @Return 明日方舟干员记录
     */
    ArknightsOperator selectOneById(@Param("id")String id);

    /**
     * 业务主键查找唯一值
     * @Param {id} ID
     * @Return 明日方舟干员记录
     */
    ArknightsOperator selectOneByUniqueKey(@Param("name") String name);

    /**
     * 根据条件取得件数
     * @Param {condition} 检索条件
     * @Return 记录数
     */
    int getCountByDto(ArknightsOperatorDto condition);

    /**
     * 根据条件取得一览
     * @Param {condition} 检索条件
     * @Return 明日方舟干员记录List
     */
    List<ArknightsOperator> selectByDto(ArknightsOperatorDto condition);

    /**
     * 新增一条数据
     * @Param {ArknightsOperator 实体Pojo
     * @Return 0:失败,1:成功
     */
    int insert(ArknightsOperator model);

    /**
     * 更新一条数据
     * @Param {ArknightsOperator 实体Pojo
     * @Return 更新件数
     */
    int update(ArknightsOperator model);

    /**
     * 通过ID删除记录
     * @Param {id} ID
     * @Return 删除件数
     */
    int delete(@Param("id")String id);

    /**
     * 自定义查询
     * @Param {condition} 扩展字段实现自定义SQL查询
     * @Return 明日方舟干员记录List
     */
    List<ArknightsOperator> customQuary(ArknightsOperatorDto condition);

}
