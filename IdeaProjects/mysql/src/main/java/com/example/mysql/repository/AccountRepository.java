package com.example.mysql.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.mysql.dto.AccountDto;
import com.example.mysql.model.Account;

/**
 * 用户Repository
 */
@Repository
public interface AccountRepository {

    /**
     * 通过ID主键查找唯一一条记录
     * @Param {id} ID
     * @Return 用户记录
     */
    Account selectOneById(@Param("id")String id);

    /**
     * 业务主键查找唯一值
     * @Param {id} ID
     * @Return 用户记录
     */
    Account selectOneByUniqueKey(@Param("loginName") String loginName,@Param("username") String username,@Param("telphone") String telphone);

    /**
     * 根据条件取得件数
     * @Param {condition} 检索条件
     * @Return 记录数
     */
    int getCountByDto(AccountDto condition);

    /**
     * 根据条件取得一览
     * @Param {condition} 检索条件
     * @Return 用户记录List
     */
    List<Account> selectByDto(AccountDto condition);

    /**
     * 新增一条数据
     * @Param {Account 实体Pojo
     * @Return 0:失败,1:成功
     */
    int insert(Account model);

    /**
     * 更新一条数据
     * @Param {Account 实体Pojo
     * @Return 更新件数
     */
    int update(Account model);

    /**
     * 通过ID删除记录
     * @Param {id} ID
     * @Return 删除件数
     */
    int delete(@Param("id")String id);

    /**
     * 自定义查询
     * @Param {condition} 扩展字段实现自定义SQL查询
     * @Return 用户记录List
     */
    List<Account> customQuary(AccountDto condition);

}
