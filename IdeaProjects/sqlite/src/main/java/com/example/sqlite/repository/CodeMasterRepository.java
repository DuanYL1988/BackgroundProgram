package com.example.sqlite.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.sqlite.model.CodeMaster;

@Repository
public interface CodeMasterRepository {

    CodeMaster selectOneById(@Param("id")Integer id);

    CodeMaster selectOneByUniqueKey();

    int getCountByDto(CodeMaster codemaster);

    List<CodeMaster> selectByDto(CodeMaster codemaster);

    int insert(CodeMaster codemaster);

    int update(CodeMaster codemaster);

    int delete(@Param("id")Integer id);

    List<CodeMaster> customQuary(CodeMaster codemaster);

}


