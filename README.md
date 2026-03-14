# 🖼️ JPG to RGB565 Little-Endian Converter for ST7789 Display

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Pillow](https://img.shields.io/badge/Pillow-9.0+-green.svg)](https://python-pillow.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🇷🇺 Русский

### 📋 Описание

Инструмент для конвертации JPG изображений в C-массив формата RGB565 little-endian для вывода на дисплеи ST7789 (240x240 пикселей).

Этот скрипт преобразует обычные JPG изображения в формат, который можно использовать с дисплеями ST7789 через функцию `ST7789_DrawImage`. Он создает двумерный C-массив `[240][240]` с 16-битными значениями в формате RGB565 little-endian.

#### Пример выходного формата:
```c
const uint16_t saber[240][240] = {
    {0x20C5, 0x28E6, 0x20C6, 0x20C6, 0x28C7, 0x20A6, 0x2907, 0x2907,
     0x28C6, 0x20A6, 0x2908, 0x20A6, 0x1884, 0x18A4, 0x3989, 0x28E6,
     ... },
    ...
};
```

### ✨ Возможности

- ✅ Конвертация JPG в RGB565 little-endian (правильный формат для ST7789)
- ✅ Автоматическое изменение размера до 240x240
- ✅ Создание .c и .h файлов
- ✅ Сохранение JPG превью для визуальной проверки
- ✅ Подробная отладка и статистика
- ✅ Создание тестового изображения с градиентом
- ✅ Дружественный вывод в консоль с эмодзи

### 🔧 Требования

- Python 3.6 или выше
- Установленные библиотеки:
  ```bash
  pip install Pillow numpy
  ```

### 📦 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/jpg-to-rgb565-converter.git
cd jpg-to-rgb565-converter
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

### 🚀 Использование

#### Базовое использование
```bash
python convert.py your_image.jpg
```

#### Создание тестового изображения
```bash
python convert.py --test
```

#### Конвертация с указанием имени массива
```bash
python convert.py photo.jpg -n my_photo
```

#### Конвертация с сохранением в конкретный файл
```bash
python convert.py image.jpg -o display/saber.c -n saber
```

#### Полный список параметров
```bash
python convert.py -h
```

**Параметры:**
- `input` - путь к JPG файлу
- `-o, --output` - выходной .c файл
- `-n, --name` - имя массива (по умолчанию: saber)
- `--test` - создать тестовое изображение с градиентом

### 📁 Структура выходных файлов

| Файл | Описание |
|------|----------|
| `имя_le.c` | C-массив с данными изображения |
| `имя_le.h` | Заголовочный файл с декларацией |
| `имя_preview.jpg` | Превью в RGB565 для визуальной проверки |

### 🎯 Использование в микроконтроллере

```c
#include "image_le.h"

void display_image(void) {
    // Вывод изображения в левом верхнем углу
    ST7789_DrawImage(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT, (const uint16_t*)image);
    
    // Или в центре дисплея
    uint16_t x = (ST7789_WIDTH - IMAGE_WIDTH) / 2;
    uint16_t y = (ST7789_HEIGHT - IMAGE_HEIGHT) / 2;
    ST7789_DrawImage(x, y, IMAGE_WIDTH, IMAGE_HEIGHT, (const uint16_t*)image);
}
```

### 🔍 Как это работает

1. **Загрузка изображения** - открывается JPG файл с помощью PIL
2. **Изменение размера** - изображение масштабируется до 240x240 пикселей
3. **Конвертация в RGB565** - каждый пиксель преобразуется:
   - Красный: 8 бит -> 5 бит
   - Зеленый: 8 бит -> 6 бит
   - Синий: 8 бит -> 5 бит
4. **Little-endian** - байты переставляются для правильного порядка
5. **Сохранение** - создаются .c, .h и preview.jpg файлы

### ⚠️ Важные замечания

- Размер данных для 240x240: **115,200 байт** (112.5 KB)
- Убедитесь, что в вашем микроконтроллере достаточно памяти
- Превью JPG показывает точное соответствие тому, что увидите на дисплее
- Если все значения нулевые - проверьте, не черное ли изображение

---

## 🇬🇧 English

### 📋 Description

A tool for converting JPG images to C array in RGB565 little-endian format for ST7789 displays (240x240 pixels).

This script converts regular JPG images into a format that can be used with ST7789 displays via the `ST7789_DrawImage` function. It creates a 2D C array `[240][240]` with 16-bit values in RGB565 little-endian format.

#### Output Example:
```c
const uint16_t saber[240][240] = {
    {0x20C5, 0x28E6, 0x20C6, 0x20C6, 0x28C7, 0x20A6, 0x2907, 0x2907,
     0x28C6, 0x20A6, 0x2908, 0x20A6, 0x1884, 0x18A4, 0x3989, 0x28E6,
     ... },
    ...
};
```

### ✨ Features

- ✅ Convert JPG to RGB565 little-endian (correct format for ST7789)
- ✅ Automatic resizing to 240x240
- ✅ Generate .c and .h files
- ✅ Save JPG preview for visual verification
- ✅ Detailed debugging and statistics
- ✅ Create test gradient image
- ✅ User-friendly console output with emojis

### 🔧 Requirements

- Python 3.6 or higher
- Required libraries:
  ```bash
  pip install Pillow numpy
  ```

### 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jpg-to-rgb565-converter.git
cd jpg-to-rgb565-converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 🚀 Usage

#### Basic Usage
```bash
python convert.py your_image.jpg
```

#### Create Test Image
```bash
python convert.py --test
```

#### Convert with Custom Array Name
```bash
python convert.py photo.jpg -n my_photo
```

#### Convert with Specific Output File
```bash
python convert.py image.jpg -o display/saber.c -n saber
```

#### Full Parameter List
```bash
python convert.py -h
```

**Parameters:**
- `input` - path to JPG file
- `-o, --output` - output .c file
- `-n, --name` - array name (default: saber)
- `--test` - create test gradient image

### 📁 Output File Structure

| File | Description |
|------|-------------|
| `name_le.c` | C array with image data |
| `name_le.h` | Header file with declaration |
| `name_preview.jpg` | RGB565 preview for visual verification |

### 🎯 Microcontroller Usage

```c
#include "image_le.h"

void display_image(void) {
    // Display image in top-left corner
    ST7789_DrawImage(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT, (const uint16_t*)image);
    
    // Or in the center of the display
    uint16_t x = (ST7789_WIDTH - IMAGE_WIDTH) / 2;
    uint16_t y = (ST7789_HEIGHT - IMAGE_HEIGHT) / 2;
    ST7789_DrawImage(x, y, IMAGE_WIDTH, IMAGE_HEIGHT, (const uint16_t*)image);
}
```

### 🔍 How It Works

1. **Load Image** - opens JPG file using PIL
2. **Resize** - scales image to 240x240 pixels
3. **Convert to RGB565** - each pixel is transformed:
   - Red: 8 bits -> 5 bits
   - Green: 8 bits -> 6 bits
   - Blue: 8 bits -> 5 bits
4. **Little-endian** - bytes are swapped for correct order
5. **Save** - creates .c, .h and preview.jpg files

### 📊 Example Output

```
🖼️  CONVERSION: test_gradient.jpg
   Size already 240x240

🔄 Converting to RGB565 little-endian...
   pixel[0,0]: RGB(  0,  0,  0) -> 0x0000
   pixel[0,1]: RGB(  1,  1,  1) -> 0x0821
   pixel[0,2]: RGB(  2,  2,  2) -> 0x0842
   ...

📊 Statistics:
   Total pixels: 57600
   Non-zero values: 57599
   Percentage non-zero: 99.99%

💾 Saving C array: test_gradient_le.c
   ✅ C array saved
   ✅ Header: test_gradient_le.h

📊 TOTAL:
   Array size: 240 x 240 = 57600 elements
   Data size: 115200 bytes (112.50 KB)
```

### ⚠️ Important Notes

- Data size for 240x240: **115,200 bytes** (112.5 KB)
- Ensure your microcontroller has enough memory
- JPG preview shows exactly what you'll see on the display
- If all values are zero - check if the image is not completely black

### 🐛 Debugging

The script includes detailed debugging information:
- File loading verification
- First pixel values
- Non-zero value statistics
- Color component ranges

## 📝 License

MIT License. Feel free to use and modify.

---

**Happy coding!** 🚀

---

*Если у вас есть вопросы или предложения, создайте issue в репозитории.*  
*If you have any questions or suggestions, please create an issue in the repository.*
