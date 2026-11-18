

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define K 3
#define ARRAY_SIZE 16

static int8_t input[48 * 96];
static int8_t weights[48 * 32 * K * K];

static int8_t layer1[48 * 96 * 6];
static int8_t layer2[24 * 48 * 16];
static int8_t layer3[12 * 24 * 32];
static int8_t layer4[6 * 12 * 48];

static void initialize_data(void)
{
    for (int i = 0; i < 48 * 96; i++)
        input[i] = (int8_t)((i * 7 + 13) % 255 - 127);

    for (int i = 0; i < (int)sizeof(weights); i++)
        weights[i] = (int8_t)((i * 3 + 5) % 255 - 127);
}

static int64_t conv_layer(
    const int8_t *src,
    int height,
    int width,
    int in_ch,
    int out_ch,
    int stride,
    int8_t *dst
)
{
    int out_h = (height + stride - 1) / stride;
    int out_w = (width + stride - 1) / stride;
    int64_t checksum = 0;

    for (int y = 0; y < out_h; y++) {
        for (int x = 0; x < out_w; x++) {
            for (int oc = 0; oc < out_ch; oc++) {
                int32_t sum = 0;

                for (int ic = 0; ic < in_ch; ic++) {
                    for (int ky = 0; ky < K; ky++) {
                        for (int kx = 0; kx < K; kx++) {
                            int iy = y * stride + ky - 1;
                            int ix = x * stride + kx - 1;
                            int8_t pixel = 0;

                            if (iy >= 0 && iy < height &&
                                ix >= 0 && ix < width) {
                                int idx = (iy * width + ix) * in_ch + ic;
                                pixel = src[idx];
                            }

                            int wi = (((oc * in_ch + ic) * K + ky) * K + kx);
                            sum += (int32_t)pixel * (int32_t)weights[wi];
                        }
                    }
                }

                int idx = (y * out_w + x) * out_ch + oc;
                dst[idx] = (int8_t)(sum >> 8);
                checksum += dst[idx];
            }
        }
    }

    return checksum;
}

int main(void)
{
    initialize_data();

    printf("Scenario A CPU-only: Highway lane keeping\\n");

    int64_t c1 = conv_layer(input, 48, 96, 1, 6, 1, layer1);
    int64_t c2 = conv_layer(layer1, 48, 96, 6, 16, 2, layer2);
    int64_t c3 = conv_layer(layer2, 24, 48, 16, 32, 2, layer3);
    int64_t c4 = conv_layer(layer3, 12, 24, 32, 48, 2, layer4);

    printf("Layer 1 output: 96x48x6, checksum=%lld\\n", (long long)c1);
    printf("Layer 2 output: 48x24x16, checksum=%lld\\n", (long long)c2);
    printf("Layer 3 output: 24x12x32, checksum=%lld\\n", (long long)c3);
    printf("Layer 4 output: 12x6x48, checksum=%lld\\n", (long long)c4);

    printf("Scenario A CPU-only workload completed successfully\\n");

    return 0;
}
