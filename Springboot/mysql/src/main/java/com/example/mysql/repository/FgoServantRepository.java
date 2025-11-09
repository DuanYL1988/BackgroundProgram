package com.example.mysql.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.mysql.dto.FgoServantDto;
import com.example.mysql.model.FgoServant;

/**
 * FGO从者Repository
 */
@Repository
public interface FgoServantRepository {

    /**
     * 通过ID主键查找唯一一条记录
     * @Param {id} ID
     * @Return FGO从者记录
     */
    FgoServant selectOneById(@Param("id")String id);

    /**
     * 业务主键查找唯一值
     * @Param {id} ID
     * @Return FGO从者记录
     */
    FgoServant selectOneByUniqueKey(@Param("id") String id);

    /**
     * 根据条件取得件数
     * @Param {condition} 检索条件
     * @Return 记录数
     */
    int getCountByDto(FgoServantDto condition);

    /**
     * 根据条件取得一览
     * @Param {condition} 检索条件
     * @Return FGO从者记录List
     */
    List<FgoServant> selectByDto(FgoServantDto condition);

    /**
     * 新增一条数据
     * @Param {FgoServant 实体Pojo
     * @Return 0:失败,1:成功
     */
    int insert(FgoServant model);

    /**
     * 更新一条数据
     * @Param {FgoServant 实体Pojo
     * @Return 更新件数
     */
    int update(FgoServant model);

    /**
     * 通过ID删除记录
     * @Param {id} ID
     * @Return 删除件数
     */
    int delete(@Param("id")String id);

    /**
     * 自定义查询
     * @Param {condition} 扩展字段实现自定义SQL查询
     * @Return FGO从者记录List
     */
    List<FgoServant> customQuary(FgoServantDto condition);

}
