package com.example.mysql.util;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.Claim;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.example.mysql.dto.AccountDto;
import com.example.mysql.model.Account;
import com.example.mysql.model.LoginUser;

public class JWTUtil {
    // 有效时间
    private static final long limitTime = 1000 * 60 * 60;
    // 算法秘钥
    private static final String signature = "1234567890123456789012345678901234567890123";

    /**
     * 对用户信息进行jwt加密并返回token
     */
    public static String createJwt(LoginUser user) {
        Account account = user.getUser();
        return JWT.create()
                .withClaim("name", account.getUsername())
                .withClaim("app", account.getApplication())
                .withClaim("company", account.getCompany())
                .withClaim("role", account.getRoleId())
                .withClaim("id", account.getId() + "")
                .withExpiresAt(new Date(System.currentTimeMillis() + limitTime)).sign(Algorithm.HMAC256(signature));
    }

    /**
     * 解密token并返回json信息的Map
     */
    public static Map<String, String> parseToken(String token) {
        JWTVerifier jwtVerifier = JWT.require(Algorithm.HMAC256(signature)).build();
        DecodedJWT decodedJWT = jwtVerifier.verify(token);
        Map<String, Claim> claims = decodedJWT.getClaims();
        Map<String, String> result = new HashMap<>();
        for (String key : claims.keySet()) {
            result.put(key, claims.get(key).asString());
        }
        return result;
    }

    /**
     * 解密token并返回Account
     */
    public static AccountDto parseTokenToAccount(String token) {
        JWTVerifier jwtVerifier = JWT.require(Algorithm.HMAC256(signature)).build();
        DecodedJWT decodedJWT = jwtVerifier.verify(token);
        Map<String, Claim> claims = decodedJWT.getClaims();
        AccountDto result = new AccountDto();
        result.setId(Integer.parseInt(claims.get("id").asString()));
        result.setUsername(claims.get("name").asString());
        result.setApplication(claims.get("app").asString());
        result.setRoleId(claims.get("role").asString());
        result.setCompany(claims.get("company").asString());
        return result;
    }

    public static String getEncodePsd(String psdInput) {
        PasswordEncoder encoder = new BCryptPasswordEncoder();
        return encoder.encode(psdInput);
    }
}
