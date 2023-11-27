package funcs

import (
	"opsx/monitorx_proxy/g"
	"time"

	"github.com/dgrijalva/jwt-go"
)

type CustomClaims struct {
	Username  string `json:"username"`
	Password  string `json:"password"`
	Timestamp int64  `json:"timestamp"`
	jwt.StandardClaims
}

// 认证token
func get_token() string {
	customClaims := &CustomClaims{
		Username:       g.Config().Server.AccessID,
		Password:       g.Config().Server.AccessKey,
		Timestamp:      time.Now().Unix(),
		StandardClaims: jwt.StandardClaims{},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, customClaims)
	tokenString, err := token.SignedString([]byte(g.Config().Server.SecretKey))
	if err != nil {
		return ""
	}
	return tokenString
}
