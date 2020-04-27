import React, { useState, useEffect, useContext } from 'react';
import '../css/PetitionList.css';
import RefreshIcon from '../icons/round_refresh_black_18dp.png';
import axios from 'axios';
import KeywordContext from '../context/Keyword.context';


// Table
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';


const PetitionList = () => {

  // Define state of wordcloud data
  const [petitions, setPetitions] = useState([]);
  const { word } = useContext(KeywordContext);

  const useStyles = makeStyles({
    table: {
      minWidth: 70
    },
  });

  const classes = useStyles();

  function createData(title, url) {
    return { title, url };
  }

  const rows = [
    createData('Frozen yoghurt', "url"),
    createData('Ice cream sandwich', "url"),
    createData('Eclair', "url"),
    createData('Cupcake', "url"),
    createData('Gingerbread', "url"),
  ];

  // Set event on refresh to load wordcloud data
  const onRefresh = () => {
    axios.get('http://localhost:5001/petition-word?keyword=코로나')
      .then(
        response => {
          let petitions = response.data['results']
          let petitions_formatted = petitions.map((petition) => ({ 'title': petition['title'], 'url': petition['url'] }))
          console.log(petitions_formatted)

          setPetitions(petitions_formatted);
        }
      )
      .catch(
        response => {
          console.log(response)
        }
      );
  };

  // Load wordcloud when this page is rendered.
  useEffect(() => {
    console.log('PetitionList rendered!');
    onRefresh();
  }, []);

  return (
    <div className="PetitionListContainer">
      <div className="Refresh" onClick={onRefresh}>
        <img src={RefreshIcon} alt="Refresh"></img>
      </div>
      <div>
        {/* {word} */}
        <TableContainer component={Paper}>
          <Table className={classes.table} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>제목</TableCell>
                <TableCell align="right">링크</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => (
                <TableRow key={row.title}>
                  <TableCell component="th" scope="row">{row.title}</TableCell>
                  <TableCell align="right">{row.url}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    </div>
  );
}

export default PetitionList;