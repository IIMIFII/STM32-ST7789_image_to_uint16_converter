from PIL import Image
import numpy as np
import os
import argparse
from datetime import datetime

def rgb888_to_rgb565_le(r, g, b):
    """
    Конвертирует RGB888 в RGB565 little-endian
    """
    # Стандартный RGB565 (big-endian)
    r5 = (r >> 3) & 0x1F
    g6 = (g >> 2) & 0x3F
    b5 = (b >> 3) & 0x1F
    
    rgb565_be = (r5 << 11) | (g6 << 5) | b5
    
    # Меняем байты для little-endian
    rgb565_le = ((rgb565_be & 0xFF) << 8) | ((rgb565_be >> 8) & 0xFF)
    
    return rgb565_le

def rgb565_le_to_rgb888(val):
    """Обратная конвертация RGB565 little-endian в RGB888 для превью"""
    # Сначала переставляем байты обратно
    val_be = ((val & 0xFF) << 8) | ((val >> 8) & 0xFF)
    
    # Распаковываем стандартный RGB565
    r5 = (val_be >> 11) & 0x1F
    g6 = (val_be >> 5) & 0x3F
    b5 = val_be & 0x1F
    
    # Конвертируем в 8 бит
    r = (r5 * 255 + 15) // 31
    g = (g6 * 255 + 31) // 63
    b = (b5 * 255 + 15) // 31
    
    return (r, g, b)

def debug_image_loading(jpg_path):
    """
    Отладочная функция для проверки загрузки изображения
    """
    print(f"\n🔍 ОТЛАДКА: Проверка загрузки {jpg_path}")
    
    try:
        if not os.path.exists(jpg_path):
            print(f"❌ Файл не существует: {jpg_path}")
            return False
        
        file_size = os.path.getsize(jpg_path)
        print(f"   Размер файла: {file_size} байт")
        
        img = Image.open(jpg_path)
        print(f"   Формат: {img.format}")
        print(f"   Размер: {img.size}")
        print(f"   Режим: {img.mode}")
        
        img_rgb = img.convert('RGB')
        first_pixel = img_rgb.getpixel((0, 0))
        print(f"   Первый пиксель (0,0): RGB{first_pixel}")
        
        w, h = img_rgb.size
        center_pixel = img_rgb.getpixel((w//2, h//2))
        print(f"   Центральный пиксель ({w//2},{h//2}): RGB{center_pixel}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке: {e}")
        return False

def jpg_to_c_array_le(jpg_path, output_path=None, width=240, height=240, 
                      array_name="saber", create_header=True, save_preview=True):
    """
    Конвертирует JPG в двумерный C-массив с RGB565 little-endian
    """
    print(f"\n🖼️  КОНВЕРТАЦИЯ: {jpg_path}")
    
    if not os.path.exists(jpg_path):
        print(f"❌ Ошибка: файл '{jpg_path}' не найден!")
        return None
    
    try:
        # Загружаем изображение
        img = Image.open(jpg_path).convert('RGB')
        
        # Изменяем размер если нужно
        if img.size != (width, height):
            print(f"   Изменение размера: {img.size} -> {width}x{height}")
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        else:
            print(f"   Размер уже {width}x{height}")
        
        # Создаем двумерный массив для RGB565
        rgb565_array = [[0 for _ in range(width)] for _ in range(height)]
        
        # Счетчик ненулевых значений
        non_zero_count = 0
        total_pixels = width * height
        
        print(f"\n🔄 Конвертация в RGB565 little-endian...")
        
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                val = rgb888_to_rgb565_le(r, g, b)
                rgb565_array[y][x] = val
                
                if val != 0:
                    non_zero_count += 1
                
                # Показываем первые несколько пикселей для отладки
                if y < 3 and x < 5:
                    print(f"   pixel[{y},{x}]: RGB({r:3d},{g:3d},{b:3d}) -> 0x{val:04X}")
        
        print(f"\n📊 Статистика:")
        print(f"   Всего пикселей: {total_pixels}")
        print(f"   Ненулевых значений: {non_zero_count}")
        print(f"   Процент ненулевых: {non_zero_count/total_pixels*100:.2f}%")
        
        if non_zero_count == 0:
            print("\n❌ ВНИМАНИЕ: Все значения нулевые!")
            print("   Это нормально только если изображение полностью черное.")
            print("   Для цветного изображения это ошибка!")
        
        # Сохраняем превью
        if save_preview:
            if output_path:
                preview_path = output_path.replace('.c', '_preview.jpg')
            else:
                base = os.path.splitext(jpg_path)[0]
                preview_path = f"{base}_preview.jpg"
            
            print(f"\n💾 Сохранение превью: {preview_path}")
            
            preview = Image.new('RGB', (width, height))
            preview_pixels = preview.load()
            
            for y in range(height):
                for x in range(width):
                    val = rgb565_array[y][x]
                    r, g, b = rgb565_le_to_rgb888(val)
                    preview_pixels[x, y] = (r, g, b)
            
            preview.save(preview_path, 'JPEG', quality=95)
            print(f"   ✅ Превью сохранено")
        
        # Сохраняем C-массив
        if output_path is None:
            base = os.path.splitext(jpg_path)[0]
            output_path = f"{base}_le.c"
        
        print(f"\n💾 Сохранение C-массива: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Заголовок файла
            f.write(f"/**\n")
            f.write(f" * RGB565 little-endian\n")
            f.write(f" * Размер: {width}x{height}\n")
            f.write(f" * Исходный файл: {os.path.basename(jpg_path)}\n")
            f.write(f" * Всего элементов: {width * height}\n")
            f.write(f" * Ненулевых значений: {non_zero_count}\n")
            f.write(f" * Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f" */\n\n")
            
            f.write(f"#include <stdint.h>\n\n")
            
            # Двумерный массив
            f.write(f"const uint16_t {array_name}[{height}][{width}] = {{\n")
            
            for y in range(height):
                f.write("    {")
                
                for x in range(width):
                    f.write(f"0x{rgb565_array[y][x]:04X}")
                    if x < width - 1:
                        f.write(", ")
                        if (x + 1) % 16 == 0:
                            f.write("\n     ")
                
                if y < height - 1:
                    f.write("},\n")
                else:
                    f.write("}\n")
            
            f.write("};\n")
        
        print(f"   ✅ C-массив сохранен")
        
        # Создаем заголовочный файл
        if create_header:
            header_path = output_path.replace('.c', '.h')
            with open(header_path, 'w', encoding='utf-8') as f:
                array_name_upper = array_name.upper()
                f.write(f"#ifndef {array_name_upper}_H\n")
                f.write(f"#define {array_name_upper}_H\n\n")
                f.write(f"#include <stdint.h>\n\n")
                f.write(f"#define {array_name_upper}_WIDTH  {width}\n")
                f.write(f"#define {array_name_upper}_HEIGHT {height}\n\n")
                f.write(f"extern const uint16_t {array_name}[{height}][{width}];\n\n")
                f.write(f"#endif // {array_name_upper}_H\n")
            
            print(f"   ✅ Заголовок: {header_path}")
        
        # Итоговая статистика
        total_bytes = width * height * 2
        print(f"\n📊 ИТОГО:")
        print(f"   Размер массива: {height} x {width} = {height * width} элементов")
        print(f"   Размер данных: {total_bytes} байт ({total_bytes/1024:.2f} KB)")
        
        # Показываем пример первых строк
        print(f"\n📝 Пример первых 2 строк:")
        for y in range(min(2, height)):
            row_preview = [f"0x{rgb565_array[y][x]:04X}" for x in range(min(8, width))]
            print(f"   строка {y}: {', '.join(row_preview)}...")
        
        return rgb565_array
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_test_image():
    """
    Создает тестовое изображение с градиентом
    """
    print("\n🎨 Создание тестового изображения...")
    
    width, height = 240, 240
    test_img = Image.new('RGB', (width, height))
    pixels = test_img.load()
    
    # Создаем градиент
    for y in range(height):
        for x in range(width):
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = int(128 + 127 * (x / width))  # Синий компонент
            pixels[x, y] = (r, g, b)
    
    test_path = "test_gradient.jpg"
    test_img.save(test_path, 'JPEG', quality=95)
    print(f"   ✅ Создано: {test_path}")
    
    return test_path

def main():
    parser = argparse.ArgumentParser(description='Конвертация JPG в RGB565 little-endian')
    parser.add_argument('input', nargs='?', help='Путь к JPG файлу')
    parser.add_argument('-o', '--output', help='Выходной .c файл', default=None)
    parser.add_argument('-n', '--name', default='saber', help='Имя массива')
    parser.add_argument('--test', action='store_true', help='Создать тестовое изображение')
    
    args = parser.parse_args()
    
    if args.test:
        test_file = create_test_image()
        jpg_to_c_array_le(test_file, array_name="test_gradient")
    
    elif args.input:
        # Сначала проверяем загрузку
        debug_image_loading(args.input)
        # Затем конвертируем
        jpg_to_c_array_le(
            args.input,
            args.output,
            array_name=args.name
        )
    
    else:
        print("Использование:")
        print("  python script.py image.jpg          # конвертировать изображение")
        print("  python script.py --test             # создать тестовое изображение")
        print("  python script.py image.jpg -n myimg # указать имя массива")

if __name__ == "__main__":
    main()