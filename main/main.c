#include <stdio.h>
#include <stdlib.h>

#include "nvs_flash.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"


#include "dht11.h"
#include "mqtt_connect.h"
#include "wifi_connect.h"

extern char temp_value[10];
extern char humidity_value[10];
extern int err;

esp_mqtt_client_config_t mqtt_cfg = {
        .broker.address = {
            .uri = MQTT_ADDRESS,
            .port = MQTT_PORT
        },
        .credentials = {
            .username = "WSVFxw7Lhodp2v6zSqYQiNHIAwvodbTXTEseYpN5ERjuafTStFyBg47HqtVruCeb",
            .client_id = "phuc",
            .authentication.password = ""
        }
    };
    
MQTT_Handler_Struct mqtt_h =
{
    .mqtt_cfg = &mqtt_cfg,
};

void app_main()
{
    esp_err_t ret;

    /* Initialize NVS. */
    ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK( ret );

    ESP_ERROR_CHECK(esp_netif_init());

    ESP_ERROR_CHECK(esp_event_loop_create_default());

    esp_netif_create_default_wifi_sta();

    wifi_init_start();
    mqtt_init_start(&mqtt_h);

}