package com.example.sqlite.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.sqlite.model.TableInfo;

@Repository
public interface TableInfoRepository {

    TableInfo selectOneById(@Param("id")Integer id);

    TableInfo selectOneByUniqueKey(@Param("tableName")String tableName,@Param("colName")String colName);

    int getCountByDto(TableInfo tableinfo);

    List<TableInfo> selectByDto(TableInfo tableinfo);

    int insert(TableInfo tableinfo);

    int update(TableInfo tableinfo);

    int delete(@Param("id")Integer id);

    List<TableInfo> customQuary(TableInfo tableinfo);

}


