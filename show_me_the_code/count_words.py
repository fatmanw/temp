#!/usr/bin/env python
#encoding:utf8

import re

demo = '''
I was six years old, my sister, Sally Kay, was a submissive three-year-old girl. For some reasons, I thought we needed to earn  some money. I decided we should "hire out" as maids. We
visited the neighbors,  offering to clean houses for them for a quater cents. Reasonable as our offer was, there were no takers. But one neighbor telephoned my mother to let her know what Mary Alice and Sally Kay were doing.

Mother had just hung up the phone when we came first into the back door into the kitchen of our apartement. "Girls," mother asked, "why were you two going around the neighborhood telling people you would clean their houses?"  Mother wasn't angry with us. In fact, we learned afterwards she was amused that we had came up with such an idea.

But, for some reason, we both denied having done any such thing. Shocked and terribly hurt that her dear little girls could be such "boldfaced liars" . Mother then told us that Mrs. Jones had just called and told her we had been to her house and said we would clean it for a quater cents .

Faced with the truth, we admitted what we had done. Mother said we have fibed, we have not told the truth.  She was sure that we knew better. She tried to explain why a fib  hurt, but she didn't feel that we really understood.

Years later, she told us that the lesson she came up with for trying to teach us to be truthful would probably have been found upon by child psychologists. The idea came to her in a flash, and a tender-hearted mother told us it was the most difficult lesson she ever taught us. It was a lesson we never forgot. After admonishing us, mother cheerfully begain preparing for lunch. As we monching on sandwhiches, she asked:" Would you two like to go to see the movies this afternoon?"

"Wow, would we ever?" We wondered what movie would be playing. Mother said:"The Matinee".

"Oh, fatastic！ We would be going to see The Matinee, would we lucky?" We got bathed and all dressed up. It was like getting ready for a birthday party. We hurried outside the apartment, not wanting to miss the bus that would take us downtown. On the landing, Mom stunned us by saying, "Girls, we are not going to the movies today." We didn't hear her right.

"What?" we objected. "What do you mean? Aren't we going to The Matinee? Mommy, you said that we are going to the Matinee. " Mother stooped and gathered us in her arms. I couldn't understand why there were tears in her eyes. We still had the time to get the bus, but hugging us, she gently explained this is a fib felt like. "It is important that what we say is true ," Mom said. "I fibbed to you just now and it felt awful to me. I don't ever want to fib again and I'm sure you don't want to fib again either. People must be able to believe each others. Do you understand? "

We assured her that we understood. We would never forget. And since we had learned a lesson, why not go to the movie to see The Matinee. There were still time. Not today. Mother told us. We would go another time. That is how over fifty years ago, my sister and I learned to be truthful. We have never forgotten how much a fib can be hurt. 
'''
filter_pattern = r',."!?'
demo = list(demo)
for i in filter_pattern:
    if i in demo:
        for j in range(demo.count(i)):
            demo.remove(i)

demo = ''.join(demo)
pattern = r'[ |\n]'
lst = re.split(pattern, demo)

print len(lst) - lst.count('')
