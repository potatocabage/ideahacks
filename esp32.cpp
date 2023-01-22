#include <iostream>
#include <curl/curl.h>
int send_data(uint8_t data[], int size)
{
    CURL *curl;
    CURLcode res;
    int ret_val = 0;
    curl = curl_easy_init();
    if (curl)
    {
        curl_easy_setopt(curl, CURLOPT_URL, "http://131.179.3.179:5500/test");
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, size);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

        res = curl_easy_perform(curl);

        if (res != CURLE_OK)
        {
            std::cout << "cURL error: " << curl_easy_strerror(res) << std::endl;
            ret_val = 1;
        }

        curl_easy_cleanup(curl);
    }
    return ret_val;
}
int main()
{
    uint8_t test[] = {1, 2, 3, 4, 5};
    send_data(test, 5);
}