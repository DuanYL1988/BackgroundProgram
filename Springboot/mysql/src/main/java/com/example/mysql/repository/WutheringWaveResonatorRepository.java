package com.example.mysql.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.mysql.dto.WutheringWaveResonatorDto;
import com.example.mysql.model.WutheringWaveResonator;

/**
 * 鸣潮(共鸣者)Repository
 */
@Repository
public interface WutheringWaveResonatorRepository {

    /**
     * 通过ID主键查找唯一一条记录
     * @Param {id} ID
     * @Return 鸣潮(共鸣者)记录
     */
    WutheringWaveResonator selectOneById(@Param("id")String id);

    /**
     * 业务主键查找唯一值
     * @Param {id} ID
     * @Return 鸣潮(共鸣者)记录
     */
    WutheringWaveResonator selectOneByUniqueKey(@Param("nameCn") String nameCn);

    /**
     * 根据条件取得件数
     * @Param {condition} 检索条件
     * @Return 记录数
     */
    int getCountByDto(WutheringWaveResonatorDto condition);

    /**
     * 根据条件取得一览
     * @Param {condition} 检索条件
     * @Return 鸣潮(共鸣者)记录List
     */
    List<WutheringWaveResonator> selectByDto(WutheringWaveResonatorDto condition);

    /**
     * 新增一条数据
     * @Param {WutheringWaveResonator 实体Pojo
     * @Return 0:失败,1:成功
     */
    int insert(WutheringWaveResonator model);

    /**
     * 更新一条数据
     * @Param {WutheringWaveResonator 实体Pojo
     * @Return 更新件数
     */
    int update(WutheringWaveResonator model);

    /**
     * 通过ID删除记录
     * @Param {id} ID
     * @Return 删除件数
     */
    int delete(@Param("id")String id);

    /**
     * 自定义查询
     * @Param {condition} 扩展字段实现自定义SQL查询
     * @Return 鸣潮(共鸣者)记录List
     */
    List<WutheringWaveResonator> customQuary(WutheringWaveResonatorDto condition);

}
