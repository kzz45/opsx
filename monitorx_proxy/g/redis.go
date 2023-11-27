package g

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/go-redis/redis/v8"
)

type RedisConn struct {
	DB       int
	TTL      int
	Port     int
	Addr     string
	Queue    string
	Password string
}

type RedisHandler struct {
	Queue       string
	DB          int
	TTL         int
	RedisClient *redis.Client
}

func RedisSetUP(obj RedisConn) RedisHandler {
	redis_client := redis.NewClient(&redis.Options{
		Network:    "tcp",
		Addr:       fmt.Sprintf("%s:%d", obj.Addr, obj.Port),
		Password:   obj.Password,
		DB:         obj.DB,
		MaxRetries: 3,
	})
	pong, err := redis_client.Ping(context.Background()).Result()
	if err != nil {
		Logger.Fatalf("connect to redis error: %s", err)
	}
	Logger.Infof("connect to redis success: %s", pong)
	return RedisHandler{Queue: obj.Queue, DB: obj.DB, TTL: obj.TTL, RedisClient: redis_client}
}

func (redis_handler *RedisHandler) RPush(key string, value interface{}) error {
	marshal_value, err := json.Marshal(value)
	if err != nil {
		return err
	}
	if _, err = redis_handler.RedisClient.RPush(context.Background(), key, marshal_value).Result(); err != nil {
		return err
	}
	return nil
}

func (redis_handler *RedisHandler) BLPop(key string) ([]string, error) {
	return redis_handler.RedisClient.BLPop(context.Background(), time.Duration(time.Second), key).Result()
}

func (redis_handler *RedisHandler) Setx(key string, value interface{}) error {
	marshal_value, err := json.Marshal(value)
	if err != nil {
		return err
	}
	if _, err := redis_handler.RedisClient.SetEX(context.Background(), key, marshal_value, time.Duration(time.Second)).Result(); err != nil {
		return err
	}
	return nil
}

func AlertsRPush(queue string, value interface{}) error {
	return local_redis_queue.RPush(queue, value)
}

func AlertsBLPop(key string) ([]string, error) {
	return local_redis_queue.BLPop(key)
}

func AlertsSetEX(queue string, value interface{}) error {
	return local_redis_queue.Setx(queue, value)
}
