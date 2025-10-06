package com.example.mysql.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.mysql.dto.CodeMasterDto;
import com.example.mysql.model.CodeMaster;

/**
 * CODE管理Repository
 */
@Repository
public interface CodeMasterRepository {

    /**
     * 通过ID主键查找唯一一条记录
     * @Param {id} ID
     * @Return CODE管理记录
     */
    CodeMaster selectOneById(@Param("id")String id);

    /**
     * 业务主键查找唯一值
     * @Param {id} ID
     * @Return CODE管理记录
     */
    CodeMaster selectOneByUniqueKey(@Param("application") String application,@Param("categoryId") String categoryId,@Param("name") String name);

    /**
     * 根据条件取得件数
     * @Param {condition} 检索条件
     * @Return 记录数
     */
    int getCountByDto(CodeMasterDto condition);

    /**
     * 根据条件取得一览
     * @Param {condition} 检索条件
     * @Return CODE管理记录List
     */
    List<CodeMaster> selectByDto(CodeMasterDto condition);

    /**
     * 新增一条数据
     * @Param {CodeMaster 实体Pojo
     * @Return 0:失败,1:成功
     */
    int insert(CodeMaster model);

    /**
     * 更新一条数据
     * @Param {CodeMaster 实体Pojo
     * @Return 更新件数
     */
    int update(CodeMaster model);

    /**
     * 通过ID删除记录
     * @Param {id} ID
     * @Return 删除件数
     */
    int delete(@Param("id")String id);

    /**
     * 自定义查询
     * @Param {condition} 扩展字段实现自定义SQL查询
     * @Return CODE管理记录List
     */
    List<CodeMaster> customQuary(CodeMasterDto condition);

}
