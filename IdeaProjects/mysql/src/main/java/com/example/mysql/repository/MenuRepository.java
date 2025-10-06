package com.example.mysql.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.mysql.dto.MenuDto;
import com.example.mysql.model.Menu;

/**
 * 菜单Repository
 */
@Repository
public interface MenuRepository {

    /**
     * 通过ID主键查找唯一一条记录
     * @Param {id} ID
     * @Return 菜单记录
     */
    Menu selectOneById(@Param("id")String id);

    /**
     * 业务主键查找唯一值
     * @Param {id} ID
     * @Return 菜单记录
     */
    Menu selectOneByUniqueKey(@Param("application") String application,@Param("menuCode") String menuCode);

    /**
     * 根据条件取得件数
     * @Param {condition} 检索条件
     * @Return 记录数
     */
    int getCountByDto(MenuDto condition);

    /**
     * 根据条件取得一览
     * @Param {condition} 检索条件
     * @Return 菜单记录List
     */
    List<Menu> selectByDto(MenuDto condition);

    /**
     * 新增一条数据
     * @Param {Menu 实体Pojo
     * @Return 0:失败,1:成功
     */
    int insert(Menu model);

    /**
     * 更新一条数据
     * @Param {Menu 实体Pojo
     * @Return 更新件数
     */
    int update(Menu model);

    /**
     * 通过ID删除记录
     * @Param {id} ID
     * @Return 删除件数
     */
    int delete(@Param("id")String id);

    /**
     * 自定义查询
     * @Param {condition} 扩展字段实现自定义SQL查询
     * @Return 菜单记录List
     */
    List<Menu> customQuary(MenuDto condition);

}
