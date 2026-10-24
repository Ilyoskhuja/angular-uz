# `debounced` bilan signallarni debounce qilish

IMPORTANT: `debounced` — [eksperimental](reference/releases#experimental). U sinab koʻrishingiz uchun tayyor, lekin barqaror boʻlishidan oldin oʻzgarishi mumkin.

Signal qiymatiga javob berishni u oʻzgarishdan toʻxtaguncha kechiktirish uchun `debounced`'dan foydalaning. U qiymati manba signalining debounce qilingan qiymatini aks ettiruvchi `Resource` qaytaradi.

```angular-ts
import {Component, debounced, resource, signal} from '@angular/core';

@Component({
  template: `
    <input (input)="query.set($event.target.value)" />

    @if (results.isLoading()) {
      <p>Searching…</p>
    }
    @for (item of results.value(); track item.id) {
      <li>{{ item.name }}</li>
    }
  `,
})
export class Search {
  query = signal('');

  debouncedQuery = debounced(this.query, 300);

  results = resource({
    params: () => this.debouncedQuery.value(),
    loader: ({params}) => fetchResults(params),
  });
}
```

`debounced` manba signalini va millisekundlarda kutish davomiyligini qabul qiladi. Qaytarilgan resource'ning `value()`'si har doim eng soʻnggi oʻrnashgan (settled) qiymatni saqlaydi, `status()` esa yangi qiymat hali kutilayotganini (pending) bildiradi.

## Debounce davomidagi holat {#status-during-debounce}

Debounce taymeri sanab turganda `status()` `'loading'` boʻladi va `value()` oldin hal boʻlgan qiymatni qaytaradi. Taymer tugaganda resource `'resolved'` holatiga oʻrnashadi. Agar manba signali xato tashlasa, resource darhol `'error'` holatiga kiradi; taymer ishga tushmaydi.

Holatlarning toʻliq roʻyxati va ularning `value()` xatti-harakati uchun [Resource holati](/guide/signals/resource#resource-status) boʻlimiga qarang.

## Maxsus kutish funksiyasi {#custom-wait-function}

Millisekundlardagi davomiylik oʻrniga `Promise<void>` qaytaruvchi funksiya uzatishingiz mumkin. Promise hal boʻlganda resource ham hal boʻladi. Agar promise oʻrnashishidan oldin manba signali oʻzgarsa, Angular oldingi promise'ni bekor qilib, yangisini boshlaydi.

```ts
debouncedQuery = debounced(query, (value, lastSnapshot) => {
  // Retry immediately after an error rather than making the user wait again.
  if (lastSnapshot.status === 'error') return;
  // Short queries get a longer delay—the user is likely still typing.
  const ms = value.length < 3 ? 500 : 200;
  return new Promise<void>((resolve) => setTimeout(resolve, ms));
});
```

Batafsil maʼlumot uchun API maʼlumotnomasidagi `DebounceTimer` turiga qarang.

## Tenglik {#equality}

Sukut boʻyicha `debounced` qiymatlarni taqqoslash uchun `Object.is`'dan foydalanadi.

Sukut boʻyicha identiklik tekshiruvi juda qattiq boʻlganda `equal` opsiyasi bilan maxsus tenglik funksiyasini bering:

```ts
debouncedFilter = debounced(filter, 200, {
  equal: (a, b) => a.category === b.category && a.minPrice === b.minPrice,
});
```

## Inyeksiya konteksti {#injection-context}

`debounced` [inyeksiya konteksti](guide/di/dependency-injection-context) ichida chaqirilishi kerak. Injector yoʻq qilinganda Angular debounce qilingan resource'ni avtomatik ravishda yoʻq qiladi va kutilayotgan har qanday taymerni bekor qiladi.

`debounced`'dan inyeksiya kontekstidan tashqarida foydalanish uchun opsiyalar orqali aniq `Injector` uzating:

```ts
@Service()
export class SearchService {
  private injector = inject(Injector);

  createDebouncedQuery(query: Signal<string>): Resource<string> {
    return debounced(query, 300, {injector: this.injector});
  }
}
```
