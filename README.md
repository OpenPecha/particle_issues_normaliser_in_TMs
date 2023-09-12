
<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<!-- Replace with 1-sentence description about what this tool is or does.-->

<h3 align="center">Normalising the particle issues in TMs </h3>
<h5>About</h5>
<p>
  We are finding issues in our machine translation training data. While creating training data, we have used botok to do some cleaning the text and segmenting them to sentences. Due to some bug in botok, our segments are containing བལྟ་བ་འི་ instead of བལྟ་བའི་. We are facing similar issues with ཨི་ལྡན་ particles ས and ལ་དོན་ particles ར་. Therefore we want to resolve these issues in our TMs.

  This repo would aim to download the training data(tibetan text corpus) and segmenting them to sentences using the already improved botok with no affix issues mentioned aboved. Then update those content to already sentenced segmented and aligned(with english texts) files but with affix issues. 

  This repo aim to update the affix issues presented in already sentence segments so the the Translation Model wont learn those mistake when learning from those segments.
</p>

## Project owner(s)

<!-- Link to the repo owners' github profiles -->

- [@tenzin3](https://github.com/tenzin3)


## Integrations

<!-- Add any intregrations here or delete `- []()` and write None-->

None
## Docs

<!-- Update the link to the docs -->

Read the docs [here](https://wiki.openpecha.org/#/dev/coding-guidelines).
