# Inyeksiya konteksti

Bogʻliqliklarni inyeksiya qilish (DI) tizimi joriy injector mavjud boʻlgan ishga tushirish vaqti kontekstiga (runtime context) tayanadi.

Bu injector'lar faqat kodni shu kontekst ichida bajarganingizda ishlaydi degani.

Inyeksiya konteksti (injection context) quyidagi holatlarda mavjud boʻladi:

- DI tizimi tomonidan yaratilgan klass, masalan `@Injectable` yoki `@Component`, yaratilayotgan paytda (`constructor` orqali).
- Bunday klasslarning maydon initsializatorlarida.
- `Provider` yoki `@Injectable`'ning `useFactory` uchun koʻrsatilgan fabrika funksiyasida.
- `InjectionToken` uchun koʻrsatilgan `factory` funksiyasida.
- Inyeksiya kontekstida ishlaydigan stek freymi (stack frame) ichida.

Qachon inyeksiya kontekstida ekaningizni bilish bogʻliqliklarni olish uchun [`inject`](api/core/inject) funksiyasidan foydalanish imkonini beradi.

NOTE: Klass konstruktorlari va maydon initsializatorlarida `inject()` ishlatishning asosiy misollari uchun [umumiy koʻrinish qoʻllanmasiga](/guide/di#where-can-inject-be-used) qarang.

## Kontekstdagi stek freymi {#stack-frame-in-context}

Baʼzi API'lar inyeksiya konteksti ichida ishlash uchun moʻljallangan. Masalan, router himoyachilari (guard) shunday. Bu servislarga murojaat qilish uchun himoyachi funksiyasi ichida [`inject`](api/core/inject) funksiyasidan foydalanish imkonini beradi.

Quyida `CanActivateFn` uchun misol keltirilgan

```ts {highlight: [3]}
const canActivateTeam: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot,
) => {
  return inject(PermissionsService).canActivate(inject(UserToken), route.params.id);
};
```

## Inyeksiya konteksti ichida ishga tushirish {#run-within-an-injection-context}

Agar inyeksiya kontekstida boʻlmagan holda funksiyani inyeksiya konteksti ichida ishga tushirishingiz kerak boʻlsa, `runInInjectionContext` funksiyasidan foydalanishingiz mumkin.
Bu `EnvironmentInjector` kabi injector'ga kirishni talab qiladi:

```ts {highlight: [7], header:"hero.service.ts"}
@Service()
export class HeroService {
  private environmentInjector = inject(EnvironmentInjector);

  someMethod() {
    runInInjectionContext(this.environmentInjector, () => {
      inject(SomeService); // Do what you need with the injected service
    });
  }
}
```

Eʼtibor bering, [`inject`](/api/core/inject) nusxani faqat injector soʻralgan tokenni hal qila olgan taqdirda qaytaradi.

## Kontekstni tekshirish {#asserts-the-context}

Angular joriy kontekst inyeksiya konteksti ekanligini tekshirish va agar unday boʻlmasa, aniq xato chiqarish uchun `assertInInjectionContext` yordamchi funksiyasini taqdim etadi. Xato xabari toʻgʻri API kirish nuqtasiga ishora qilishi uchun chaqiruvchi funksiyaga havolani uzating. Bu sukut boʻyicha chiqariladigan umumiy inyeksiya xatosiga nisbatan aniqroq va amaliy xabar beradi.

```ts
import {ElementRef, assertInInjectionContext, inject} from '@angular/core';

export function injectNativeElement<T extends Element>(): T {
  assertInInjectionContext(injectNativeElement);
  return inject(ElementRef).nativeElement;
}
```

Shundan soʻng bu yordamchi funksiyani **inyeksiya kontekstidan** (konstruktor, maydon initsializatori, provider fabrikasi yoki `runInInjectionContext` orqali bajarilgan kod) chaqirishingiz mumkin:

```ts
import {Component, inject} from '@angular/core';
import {injectNativeElement} from './dom-helpers';

@Component({/* … */})
export class PreviewCard {
  readonly hostEl = injectNativeElement<HTMLElement>(); // Field initializer runs in an injection context.

  onAction() {
    const anotherRef = injectNativeElement<HTMLElement>(); // Fails: runs outside an injection context.
  }
}
```

## DI'dan kontekstdan tashqarida foydalanish {#using-di-outside-of-a-context}

Agar [`inject`](api/core/inject) yoki `assertInInjectionContext` funksiyasini inyeksiya kontekstidan tashqarida chaqirsangiz, Angular [NG0203 xatosini](/errors/NG0203) chiqaradi.
