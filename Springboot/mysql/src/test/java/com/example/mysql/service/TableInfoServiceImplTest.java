package com.example.mysql.service;

import java.util.List;
import java.util.Map;

import com.example.mysql.dto.FireemblemHeroDto;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.example.mysql.dto.AccountDto;
import com.example.mysql.model.Account;
import com.example.mysql.model.LoginUser;
import com.example.mysql.model.Menu;
import com.example.mysql.repository.AccountRepository;
import com.example.mysql.util.JWTUtil;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

@SpringBootTest
public class TableInfoServiceImplTest {

    @Autowired
    AccountRepository accountDao;

    @Autowired
    TableInfoServiceImpl service;

    @Autowired
    MenuServiceImpl menuService;

    @Test
    public void testServiceMethod() throws JsonProcessingException {
        Map<String, Object> result = service.getList("FIREEMBLEM_HERO");
        ObjectMapper mapper = new ObjectMapper();
        System.out.println(mapper.writeValueAsString(result));
    }

    @Test
    public void testGetLoginUserMenu(){
        Account account = accountDao.selectOneById(String.valueOf(1));
        LoginUser user = new LoginUser();
        user.setUser(account);
        String token = JWTUtil.createJwt(user);
        System.out.println("Step.1 => 创建用户登录jwt:" + token);
        // 转换
        AccountDto afterUser = JWTUtil.parseTokenToAccount(token);
        Map<String, List<Menu>> menuGroup = menuService.getAllMenu(afterUser);
        System.out.println("Step.2 => 登录用户的菜单");
        for (String parentCode : menuGroup.keySet()){
            System.out.println("    " + parentCode);
            for(Menu childMenu: menuGroup.get(parentCode)) {
                System.out.println("        " + childMenu.getMenuName());
            }
        }
    }

}
