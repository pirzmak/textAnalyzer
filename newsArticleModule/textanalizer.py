import nltk
from collections import Counter
from nltk.corpus import stopwords

sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""

stopwords = stopwords.words('english')


def bags_of_words(text):
    text = text.lower()

    from nltk.tokenize import word_tokenize
    # tokenize
    nltk.download('punkt')
    tokenized = word_tokenize(text)

    correct_word = list(map(lambda w: normalise(w), tokenized))

    return list(filter(lambda w: acceptable_word(w), correct_word))


def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        yield subtree.leaves()


def normalise(word):
    word = word.lower()
    word = lemmatizer.lemmatize(word)
    word = stemmer.stem(word)
    return word


def acceptable_word(word):
    accepted = bool(2 <= len(word) <= 40
                    and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [normalise(w) for w, t in leaf if acceptable_word(w)]
        yield term


def get_nouns_phrases(text):
    chunker = nltk.RegexpParser(grammar)
    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)

    tree = chunker.parse(postoks)

    return get_terms(tree)


words = bags_of_words(
    'iPadOS impressions: flexible and powerful, but is it intuitive?\n- The Verge\nSkip to main content\nWe use cookies and other tracking technologies to improve your browsing experience on our site, show personalized content and targeted ads, analyze site traffic, and understand where our audience is coming from. To find out more or to opt-out, please read our Cookie Policy. In addition, please read our Privacy Policy, which has also been updated and became effective May 23rd, 2018.\nBy choosing I Accept, you consent to our use of cookies and other tracking technologies.\nI Accept\nclock\nmenu\nmore-arrow\nno\nyes\nLog In or Sign Up\nLog In\nSign Up\nTech\nReviews\nScience\nCreators\nEntertainment\nVideo\nFeatures\nPodcasts\nNewsletters\nStore\nMore\nTech\nVideo\nAmazon\nApple\nFacebook\nGoogle\nMicrosoft\nSamsung\nTesla\nAI\nCars\nCybersecurity\nMobile\nPolicy\nPrivacy\nScooters\nAll Tech\nReviews\nPhones\nLaptops\nHeadphones\nCameras\nTablets\nSmartwatches\nSpeakers\nDrones\nAccessories\nThis is my Next\nHow-to\nGood Deals\nMore from Verge Guidebook\nScience\nVideo\nSpace\nNASA\nSpaceX\nHealth\nEnergy\nEnvironment\nAll Science\nCreators\nYouTube\nInstagram\nAdobe\nKickstarter\nTumblr\nArt Club\nCameras\nPhotography\nWhat’s in your bag?\nAll Creators\nEntertainment\nFilm\nTV\nGames\nFortnite\nGame of Thrones\nBooks\nComics\nMusic\nAll Entertainment\nVideo\nFeatures\nPodcasts\nNewsletters\nStore\n✕\nProcessor with Dieter Bohn\nApple\nFeatured Videos\niPadOS impressions: flexible and powerful, but is it intuitive?\nNew,\n104\ncomments\nApple fixed a lot of annoyances, at the very least\nBy\nDieter Bohn@backlon\nJun\n6, 2019, 10:00am EDT\nShare\nTweet\nShare\nShare\niPadOS impressions: flexible and powerful, but is it intuitive?\nshare\ntweet\nLinkedin\nReddit\nPocket\nFlipboard\nEmail\nThis article is part of a series of articles titled\nProcessor with Dieter Bohn is a YouTube show that takes a deeper look at how consumer technology is changing and how we should think about our gadgets as people, not just as users. Subscribe here.\nEarlier this week at WWDC, I finally got a chance to sit down and actually use iPadOS on an iPad Pro. The purpose of the meeting was ostensibly to walk me through the new features, but I greedily grabbed the iPad and started tapping, swiping, and opening web pages — listening and talking about what was new all the while. Turns out that, just like the new OS on the iPad, I can multitask better than I expected.\nJamming through the new features on iPadOS was like a greatest hits album of iPad Pro complaints that have been resolved. External USB drives, direct access to drives for Lightroom, and a desktop-class browser all felt like direct responses to our iPad Pro review last year.\nOther annoying things have also been fixed, too. For example, you can finally (finally!) directly change Wi-Fi networks and Bluetooth devices right from the appropriate buttons in Control Center. Apple is also finally bringing quick actions and pop-up web previews to the iPad — thanks in part to its decision to basically merge 3D touch and long-presses.\nVjeran Pavic / The Verge\nBut as I mentioned when I wrote about how Google Docs worked surprisingly well in Safari, I walked away from my brief time with iPadOS unsure exactly how much Apple has really changed. Did it simply fix all the things people have complained about for years, one-by-one? Or is Apple trying to architect a more fundamental overhaul that would make the iPad feel much less constrained by design?\nYou can certainly argue it both ways, based on what we’ve seen so far. For example, Apple completely changed how the USB stack works in iOS, ensuring it’s properly sandboxed in user space, while building in support for several different USB protocols. It should be fairly trivial for Apple to expand that in powerful ways going forward.\nI’m similarly pleased with the much-simplified cursor control system on the iPad for text editing. One clever thing you might not have seen: if you move your finger really quickly outside the text when moving the cursor, it gets gigantified so you can see where it is and makes it easier to quickly move it to a different paragraph.\nI also see a lot of effort going into the iPad’s new windowing system. Yes, the basics of how you arrange windows are the same: split screen and slideover. But the ability to fan out those slideover apps or swipe through them turns a sort-of-nice feature into what amounts to having a spare iPhone sitting on the right hand side of your screen. And since apps can spawn multiple windows, Apple added the ability to get an overview of each app’s open windows quickly, which creates a new kind of multitasking workflow.\nVjeran Pavic / The Verge\nOf course, all these windowing tricks are only good if apps support them — and right now, many key iPad apps do not (looking at you, Google). But Apple tells me that sometime next year it will change the rules so that supporting the iPadOS window system will be mandatory for all iPad apps. I’m glad.\nBut ever since Monday, I’ve kept coming back to the same idea: the new gestures that Apple added are really great but feel a little tacked-on. You can use three fingers to do a bunch of “manipulation” stuff: pinch and spread for copy and paste, swipe for undo or redo. They make sense when you learn them, but you really do have to learn them in a way that wasn’t necessary before.\nI don’t think they’re very discoverable. You’d have to do a lot of weird experimentation with multiple fingers to find these new gestures on your own, although Apple tells me it will offer onboarding tutorials for some of them. The company famously made little tutorial videos when it launched the iPhone, but this time around these new power-user gestures are much more complicated and much less easy to figure out on your own.\nVjeran Pavic / The Verge\nWhat I’m getting to is these three-finger gestures are unintuitive, but when I say “unintuitive” I mean something completely different from the common understanding of it. I think that when most people hear “intuitive,” they think “innately understood by humans with no training necessary.” I think that’s wrong, at least when it comes to user interfaces.\nI don’t think any user interface — whether it’s a computer or a bicycle — is the sort of thing that humans just innately understand. Nearly everything we do requires training and learning. The difference between an intuitive interface and an unintuitive one is how that learning happens.\nWith intuitive interfaces, you don’t notice that the learning is happening. One skill flows naturally into the next, more complex skill on a relatively easy learning curve. Take the classic desktop interface: if you step back and look, it’s actually deeply weird! It only feels normal because it’s been around for 35 years. However, it is intuitive: you learn left click, then discover right click, then see keyboard shortcuts listed. Each skill leads somewhat naturally to the next, and there are little hints that these extra tools exist all over the interface, inviting you to try them out whenever you want.\nVjeran Pavic / The Verge\nUnintuitive interfaces require training: like classes or little tutorial videos showing you how to do stuff that you’ll hopefully remember later. As I note in the video above, different types of languages are a good example of intuitive / unintuitive divide. Math as a language is unintuitive for most people: you need to take classes to figure it out. But natural languages like the one you speak are intuitive — at least for children: they learn them without even noticing it’s happening just because their parents talk to them.\nThat doesn’t mean that unintuitive interfaces are inherently bad, either. I want to be super clear about that. If an interface requires you to do a little training but feels internally consistent, you are more likely to remember how things work down the road. And it seems as though the iPadOS user interface does have some consistency, though it’s not perfect yet:\nOne finger: open or make a window with the thing you’re tapping or dragging\nTwo fingers: select stuff (right now this only works in lists I believe? Apple should expand that)\nThree fingers: act the thing I’ve selected, or undo my last act\nFour fingers: Go home\nThis seems like it has the potential to be a durable, flexible, and powerful user interface system, one that can work really well for people picking up an iPad for the first time and for power users who are replacing their laptops with iPads. But the real trick is having the interface teach people to go from the first group to the second group without having to focus on teaching themselves how iPadOS works.\nMaybe I’m wrong, and when we see more people using it beyond the developers who are brave enough to install the first beta, these advanced gestures will come really naturally. If they don’t, that doesn’t mean the new gestures are bad — but it might mean they’re not very intuitive.\nThe Verge on YouTube\nExclusive first looks at new tech, reviews, and shows like In the Making.\nSubscribe!\nIn this Storystream\nWWDC 2019: the latest news from Apple’s big developer conference\nApple’s new sign-in button is built for a post-Cambridge Analytica world\niPadOS impressions: flexible and powerful, but is it intuitive?\nApple will permanently remove Dashboard in macOS Catalina\nView all 42 stories\nNext Up In\nTech\nGood Deals\nYou can still save $200 on a Samsung Galaxy S10E\nNew deals, plus a few Father’s Day offers that are still active\nGoogle’s loud Home Max speaker is $40 off for Verge readers\nA handful of exclusive deals for you\nThe Google Pixel 3 and 3 XL are $300 off at B&H Photo\nThe sale price is limited to 64GB, ‘not pink’ models\nHollow Knight for $7.50 on the Switch is E3 2019’s best deal\nPlay this game\nAdding a 512GB microSD card to your Nintendo Switch is cheaper than ever\nStarting at $80.99, today only\nMore in Good Deals\nVerge3.0_Logomark_Color_1\nSign up for the\nnewsletter\nCommand Line\nCommand Line delivers daily updates from the near-future.\nemail address...\nSubscribe\nBy signing up, you agree to our Privacy Policy and European users agree to the data transfer policy.\nThis Article has a component height of 36. The sidebar size is long.\nLoading comments...\nChorus\nTerms of Use\nPrivacy Policy\nCookie Policy\nGDPR Commitment\nCommunications Preferences\nContact\nTip Us\nCommunity Guidelines\nAbout\nEthics Statement\nAll Systems Operational\nCheck out our status page for more details.\nVox Media\nAdvertise with us\nJobs @ Vox Media\n© 2019 Vox Media, Inc. All Rights Reserved\ntweet\nshare')

counts = Counter(words)

print("\n")
print("TEST")
print(counts)
