#!/usr/bin/env python3
"""
Script de prueba de integración para verificar que todas las funcionalidades de seguridad funcionan correctamente.
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """Prueba que todos los módulos se importan correctamente."""
    print("🔍 Probando imports...")

    try:
        # Importar utilidades de seguridad
        from app.utils.security import (
            sanitize_input,
            validate_password_strength,
            validate_xss_safe,
            validate_sql_injection_safe,
            rate_limit_check
        )
        print("✅ Utilidades de seguridad importadas")

        # Importar configuración
        from app.config.security_config import security_config
        print("✅ Configuración de seguridad importada")

        # Importar middleware
        from app.middleware.security import add_security_middleware
        print("✅ Middleware de seguridad importado")

        # Importar rutas seguras
        from app.routes.users_secure import router
        print("✅ Rutas de usuario seguras importadas")

        return True

    except Exception as e:
        print(f"❌ Error en imports: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_security_functions():
    """Prueba las funciones de seguridad básicas."""
    print("\n🔍 Probando funciones de seguridad...")

    try:
        from app.utils.security import (
            sanitize_input,
            validate_password_strength,
            validate_xss_safe,
            validate_sql_injection_safe
        )

        # Prueba sanitización
        malicious_data = {
            'name': '<script>alert("xss")</script>John',
            'email': 'john@example.com'
        }
        sanitized = sanitize_input(malicious_data)
        assert '<script>' not in sanitized['name'], "XSS no fue sanitizado"
        print("✅ Sanitización de entrada funciona")

        # Prueba validación de contraseña
        weak_pwd = validate_password_strength('weak')
        strong_pwd = validate_password_strength('MySecurePass123!')

        assert weak_pwd['overall'] == False, "Contraseña débil no fue rechazada"
        assert strong_pwd['overall'] == True, "Contraseña fuerte no fue aceptada"
        print("✅ Validación de contraseña funciona")

        # Prueba detección XSS
        safe_text = validate_xss_safe('Normal text')
        xss_text = validate_xss_safe('<script>alert(1)</script>')

        assert safe_text == True, "Texto seguro fue marcado como peligroso"
        assert xss_text == False, "Texto XSS no fue detectado"
        print("✅ Detección XSS funciona")

        # Prueba detección SQL injection
        safe_sql = validate_sql_injection_safe('Normal query')
        sql_injection = validate_sql_injection_safe("'; DROP TABLE users; --")

        assert safe_sql == True, "Consulta segura fue marcada como peligrosa"
        assert sql_injection == False, "SQL injection no fue detectado"
        print("✅ Detección SQL injection funciona")

        return True

    except Exception as e:
        print(f"❌ Error en funciones de seguridad: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Prueba la configuración de seguridad."""
    print("\n🔍 Probando configuración...")

    try:
        from app.config.security_config import security_config

        # Verificar valores por defecto
        assert security_config.RATE_LIMIT_REQUESTS_PER_MINUTE == 60
        assert security_config.PASSWORD_MIN_LENGTH == 8
        assert security_config.MAX_FILE_SIZE == 5 * 1024 * 1024
        print("✅ Configuración por defecto correcta")

        # Verificar políticas de contraseña
        assert security_config.PASSWORD_REQUIRE_UPPERCASE == True
        assert security_config.PASSWORD_REQUIRE_LOWERCASE == True
        assert security_config.PASSWORD_REQUIRE_DIGITS == True
        print("✅ Políticas de contraseña configuradas")

        return True

    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_middleware_structure():
    """Prueba la estructura del middleware."""
    print("\n🔍 Probando estructura del middleware...")

    try:
        from app.middleware.security import (
            RateLimitMiddleware,
            SecurityHeadersMiddleware,
            XSSProtectionMiddleware,
            SQLInjectionProtectionMiddleware,
            CSRFProtectionMiddleware
        )

        # Verificar que las clases existen y tienen métodos necesarios
        assert hasattr(RateLimitMiddleware, 'dispatch'), "RateLimitMiddleware no tiene dispatch"
        assert hasattr(SecurityHeadersMiddleware, 'dispatch'), "SecurityHeadersMiddleware no tiene dispatch"
        assert hasattr(XSSProtectionMiddleware, 'dispatch'), "XSSProtectionMiddleware no tiene dispatch"
        assert hasattr(SQLInjectionProtectionMiddleware, 'dispatch'), "SQLInjectionProtectionMiddleware no tiene dispatch"
        assert hasattr(CSRFProtectionMiddleware, 'dispatch'), "CSRFProtectionMiddleware no tiene dispatch"
        print("✅ Middleware tiene estructura correcta")

        return True

    except Exception as e:
        print(f"❌ Error en estructura del middleware: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routes_structure():
    """Prueba la estructura de las rutas seguras."""
    print("\n🔍 Probando estructura de rutas...")

    try:
        from app.routes.users_secure import router

        # Verificar que el router existe
        assert router is not None, "Router no existe"
        assert router.prefix == "/users", f"Router prefix incorrecto: {router.prefix}"
        print("✅ Router de usuarios configurado correctamente")

        # Verificar que tiene rutas
        routes = [route for route in router.routes]
        assert len(routes) > 0, "No hay rutas definidas"
        print(f"✅ Router tiene {len(routes)} rutas definidas")

        return True

    except Exception as e:
        print(f"❌ Error en estructura de rutas: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas."""
    print("🚀 Iniciando pruebas de integración de seguridad...\n")

    tests = [
        ("Imports", test_imports),
        ("Funciones de Seguridad", test_security_functions),
        ("Configuración", test_configuration),
        ("Middleware", test_middleware_structure),
        ("Rutas", test_routes_structure),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")

    print(f"\n📊 Resultados: {passed}/{total} pruebas pasaron")

    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La implementación de seguridad está funcionando correctamente.")
        return 0
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    exit(main())
