# Robust-Optimization-of-delivery-system

Liczba Klientów - 1000 ( lokazliazja wrocław)

Lizba Dostawców( Rolników) - 100 ( Promień lokalizacji 50km od wrocławia losowo na mapie )

Średnio każdy klient zamawia 4 razy misięcznie od losowego rolnika o wartości z naszym zyskiem 10zł wiec zysk to 40 000 meiesięcznie



Koszt utrzymania paczkoPunktu 1000zł miesięcznie, Paczko punkt nie może być dalej niż 20km od każdego rolnika 

1 przesyłka - 6,36, czyli jeśli nadana przesyłka jest tylko jedna, to zysk z tej przesyłki to 10-6,36 = 3,64
2 przesyłki - 5,71
3 przesyłki - 5,07
4 przesyłki - 4,44
5 przesyłek - 0

Paczkopunkty mogą być w miejscu jednego z rolników, jeśli rolnik jest paczkopunktem to nie pobieramy od niego opłaty czyli nie mamy zysku z transakcji zleconych do niego 

Ograniczenia, musi być tyle paczkopunktów, żeby żaden rolnik nie był dalej od paczkopunktu niz 10km 

Optymalizacja, rozmieszczenie paczkopunktów oraz ich ilość aby maksymalizować zysk


<!-- 98% paczek dociera w jeden dzień

Jeśli złożone zamówieie jest do godziny 12:00 ( czas nadania do 14:00) to dostawa następnego dnia w 98% przypadków -->

Zmienne decyzyjne
x_j {0,1} - zmienna decyzyjna czy w miejscu rolnika jest paczkopunkt( nie pobieramy zysku z tego rolnika)
x_j = 1 jeśli w miejscu rolnika jest paczkopunkt( rolnik nie będzie generował zysku)
x_j = 0 jeśi w miejscu rolnika nie ma paczkopunktu

Dane wejsciowe 
N = liczba rolników
R_j = współrzędne rolnika 
D_ij = odległość między rolnikiem i i j (w km)

Ograniczenia
Dla każdego rolnika ( i ), musi istnieć paczkopunkt w miejscu rolnika ( j ), tak aby odległość między nimi była mniejsza lub równa 10 km i paczkomat jest tam ustawiony (czyli ( x_j = 1 )).

